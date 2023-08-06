# !/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import docker
import six
import json

from girder import logger
from girder.constants import AccessType
from girder.utility.model_importer import ModelImporter
from girder_jobs.constants import JobStatus
from .models import DockerImageItem, DockerImageError, \
    DockerImageNotFoundError


def deleteImage(job):
    """
    Deletes the docker images specified in the job from the local machine.
    Images are forcefully removed (equivalent to docker rmi -f)
    :param job: The job object specifying the docker images to remove from
    the local machine

    """

    jobModel = ModelImporter.model('job', 'jobs')

    jobModel.updateJob(
        job,
        log='Started to Delete Docker images\n',
        status=JobStatus.RUNNING,
    )
    docker_client = None
    try:
        deleteList = job['kwargs']['deleteList']
        error = False

        try:
            docker_client = docker.from_env(version='auto')

        except docker.errors.DockerException as err:
            logger.exception('Could not create the docker client')
            jobModel.updateJob(
                job,
                log='Failed to create the Docker Client\n' + str(err) + '\n',
                status=JobStatus.ERROR,
            )
            raise DockerImageError('Could not create the docker client')

        for name in deleteList:
            try:
                docker_client.images.remove(name, force=True)

            except Exception as err:
                logger.exception('Failed to remove image')
                jobModel.updateJob(
                    job,
                    log='Failed to remove image \n' + str(err) + '\n',
                    status=JobStatus.RUNNING,
                )
                error = True
        if error is True:
            jobModel.updateJob(
                job,
                log='Failed to remove some images',
                status=JobStatus.ERROR,
                notify=True,
                progressMessage='Errors deleting some images'
            )
        else:

            jobModel.updateJob(
                job,
                log='Removed all images',
                status=JobStatus.SUCCESS,
                notify=True,
                progressMessage='Removed all images'
            )
    except Exception as err:
        logger.exception('Error with job')
        jobModel.updateJob(
            job,
            log='Error with job \n ' + str(err) + '\n',
            status=JobStatus.ERROR,

        )
    finally:
        if docker_client:
            docker_client.close()


def findLocalImage(client, name):
    """
    Checks if the docker image exist locally
    :param name: The name of the docker image

    :returns id: returns the docker image id
    """
    try:
        image = client.images.get(name)
    except Exception:
        return None
    return image.id


def jobPullAndLoad(job):
    """
    Attempts to cache metadata on images in the pull list and load list.
    Images in the pull list are pulled first, then images in both lists are
    queried for there clis and each cli's xml description. The clis and
    xml data is stored in the girder mongo database
    Event Listeners assume the job is done when the job status
     is ERROR or SUCCESS.
    Event listeners check the jobtype to determine if a job is Dockerimage
    related
    """
    try:
        jobModel = ModelImporter.model('job', 'jobs')
        userModel = ModelImporter.model('user')
        folderModel = ModelImporter.model('folder')
        user = userModel.load(job['userId'], level=AccessType.READ)
        baseFolder = folderModel.load(job['kwargs']['folder'], user=user, level=AccessType.WRITE)

        loadList = job['kwargs']['nameList']

        errorState = False

        notExistSet = set()
        jobModel.updateJob(
            job,
            log='Started to Load Docker images\n',
            status=JobStatus.RUNNING,
        )
        try:
            docker_client = docker.from_env(version='auto')

        except docker.errors.DockerException as err:
            logger.exception('Could not create the docker client')
            jobModel.updateJob(
                job,
                log='Failed to create the Docker Client\n' + str(err) + '\n',
            )
            raise DockerImageError('Could not create the docker client')

        pullList = [name for name in loadList if not findLocalImage(docker_client, name)]
        loadList = [name for name in loadList if name not in pullList]

        try:
            pullDockerImage(docker_client, pullList)
        except DockerImageNotFoundError as err:
            errorState = True
            notExistSet = set(err.imageName)
            jobModel.updateJob(
                job,
                log='could not find the following '
                    'images\n' + '\n'.join(notExistSet) + '\n',
                status=JobStatus.ERROR,
            )
        images, loadingError = loadMetadata(jobModel, job, docker_client, pullList,
                                            loadList, notExistSet)
        for name, cli_dict in images:
            docker_image = docker_client.images.get(name)
            DockerImageItem.saveImage(name, cli_dict, docker_image, user, baseFolder)
        if errorState is False and loadingError is False:
            newStatus = JobStatus.SUCCESS
        else:
            newStatus = JobStatus.ERROR
        jobModel.updateJob(
            job,
            log='Finished caching Docker image data\n',
            status=newStatus,
            notify=True,
            progressMessage='Completed caching docker images'
        )
    except Exception as err:
        logger.exception('Error with job')
        jobModel.updateJob(
            job,
            log='Error with job \n ' + str(err) + '\n',
            status=JobStatus.ERROR,
        )


def loadMetadata(jobModel, job, docker_client, pullList, loadList, notExistSet):
    """
    Attempt to query preexisting images and pulled images for cli data.
    Cli data for each image is stored and returned as a sing DockerCache Object

    :param jobModel: Singleton JobModel used to update job status
    :param job: The current job being executed
    :param docker_client: An instance of the Docker python client
    :param pullList: The list of images that the job attempted to pull
    :param loadList: The list of images to be queried that were already on the
    local machine
    :notExistSet: A subset of the pullList that didnot exist on the Docker
     registry
    or that could not be pulled

    :returns:DockerCache Object containing cli information for each image
    and a boolean indicating whether an error occurred
    """
    # flag to indicate an error occured
    errorState = False
    images = []
    for name in pullList:
        if name not in notExistSet:
            jobModel.updateJob(
                job,
                log='Image %s was pulled successfully \n' % name,

            )

            try:
                cli_dict = getCliData(name, docker_client, jobModel, job)
                images.append((name, cli_dict))
                jobModel.updateJob(
                    job,
                    log='Got pulled image %s metadata \n' % name

                )
            except DockerImageError as err:
                jobModel.updateJob(
                    job,
                    log='Error with recently pulled image %s\n%s\n' % (name, err),
                    status=JobStatus.ERROR
                )
                errorState = True

    for name in loadList:
        # create dictionary and load to database
        try:
            cli_dict = getCliData(name, docker_client, jobModel, job)
            images.append((name, cli_dict))
            jobModel.updateJob(
                job,
                log='Loaded metadata from pre-existing local image %s\n' % name
            )
        except DockerImageError as err:
            jobModel.updateJob(
                job,
                log='Error with recently loading pre-existing image %s\n%s\n' % (name, err),
                status=JobStatus.ERROR
            )
            errorState = True
    return images, errorState


def getDockerOutput(imgName, command, client):
    """
    Data from each docker image is collected by executing the equivalent of a
    docker run <imgName> <command/args>
    and collecting the output to standard output
    :param imgName: The name of the docker image
    :param command: The commands/ arguments to be passed to the docker image
    :param client: The docker python client
    """
    cont = None
    try:
        cont = client.containers.create(image=imgName, command=command)
        cont.start()
        ret_code = cont.wait()
        if isinstance(ret_code, dict):
            ret_code = ret_code['StatusCode']
        logs = cont.logs(stdout=True, stderr=False, stream=False)
        cont.remove()
    except Exception as err:
        if cont:
            try:
                cont.remove()
            except Exception:
                pass
        logger.exception(
            'Attempt to docker run %s %s failed', imgName, command)
        raise DockerImageError(
            'Attempt to docker run %s %s failed ' % (
                imgName, command) + str(err), imgName)
    if ret_code != 0:
        raise DockerImageError(
            'Attempt to docker run %s %s failed' % (imgName, command), imgName)
    return logs


def getCliData(name, client, jobModel, job):
    try:
        cli_dict = getDockerOutput(name, '--list_cli', client)
        # contains nested dict
        # {<cliname>:{type:<type>}}
        if isinstance(cli_dict, six.binary_type):
            cli_dict = cli_dict.decode('utf8')
        cli_dict = json.loads(cli_dict)

        for key, info in six.iteritems(cli_dict):
            desc_type = info.get('desc-type', 'xml')
            cli_desc = getDockerOutput(name, '%s --%s' % (key, desc_type), client)

            if isinstance(cli_desc, six.binary_type):
                cli_desc = cli_desc.decode('utf8')

            cli_dict[key][desc_type] = cli_desc
            jobModel.updateJob(
                job,
                log='Got image %s, cli %s metadata\n' % (name, key),
                status=JobStatus.RUNNING,
            )
        return cli_dict
    except Exception as err:
        logger.exception(
            'Error getting %s cli data from image', name)
        raise DockerImageError(
            'Error getting %s cli data from image ' % (name) + str(err))


def pullDockerImage(client, names):
    """
    Attempt to pull the docker images listed in names. Failure results in a
    DockerImageNotFoundError being raised

    :params client: The docker python client
    :params names: A list of docker images to be pulled from the Dockerhub
    """
    imgNotExistList = []
    for name in names:
        try:
            client.images.pull(name)
            # some invalid image names will not be pulled but the pull method
            # will not throw an exception so the only way to confirm if a pull
            # succeeded is to attempt a docker inspect on the image
            client.images.get(name)
        except Exception:
            imgNotExistList.append(name)
    if len(imgNotExistList) != 0:
        raise DockerImageNotFoundError('Could not find multiple images ',
                                       image_name=imgNotExistList)
