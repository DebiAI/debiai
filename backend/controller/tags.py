#############################################################################
# Imports
#############################################################################
# import utils.debiaiUtils as debiaiUtils
# import utils.debiai.tags as tagsUtils
import utils.utils as utils

#############################################################################
# Tag Management
#############################################################################


def get_tags(dataProviderId, projectId):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    return tagsUtils.getTags(projectId), 200


def get_tag(dataProviderId, projectId, tagId):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    tag = tagsUtils.getTagById(dataProviderId, projectId, tagId)
    if not tag:
        return "tag " + tagId + " not found", 404
    return tag, 200


def post_tag(dataProviderId, projectId, data):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    # Save or update tag
    return tagsUtils.updateTag(dataProviderId, projectId, data["tagName"], data["tagHash"])


def delete_tag(dataProviderId, projectId, tagId):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    if not tagsUtils.getTagById(dataProviderId, projectId, tagId):
        return "tag " + tagId + " not found", 404

    # Delete tag
    return tagsUtils.deleteTag(dataProviderId, projectId, tagId)


def get_tag_sample_tree(dataProviderId, projectId, tagId, tagValue):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    if not tagsUtils.getTagById(dataProviderId, projectId, tagId):
        return "tag " + tagId + " not found", 404

    # Get samples hash
    samplesHash = tagsUtils.getSamplesHash(dataProviderId, projectId, tagId, tagValue)

    # Converting samples hash into path
    hashList = debiaiUtils.getHashmap(projectId)
    for i in range(len(samplesHash)):
        samplesHash[i] = hashList[samplesHash[i]]

    # Get tree
    tree = debiaiUtils.getBlockTreeFromSamples(dataProviderId, projectId, samplesHash)
    return tree, 200
