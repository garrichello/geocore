
from django.utils.translation import get_language

from .models import (LevelI18N, LevelsGroup, Resolution,
                     Scenario, TimeStepI18N, UnitsI18N)


def get_resolutions(collection_id):
    return Resolution.objects.filter(dataset__collection_id=collection_id).distinct()

def get_scenarios(collection_id, resolution_id):
    return Scenario.objects.filter(dataset__collection_id=collection_id, dataset__resolution_id=resolution_id)

def get_timesteps(parameter_id):
    return TimeStepI18N.objects.filter(
        language__code=get_language(), time_step__specificparameter__parameter_id=parameter_id).distinct()

def get_levelsgroups(parameter_id, time_step_id):
    return LevelsGroup.objects.filter(
        specificparameter__parameter_id=parameter_id, specificparameter__time_step_id=time_step_id)

def get_levels(lvsgroup_id):
    units = UnitsI18N.objects.filter(
        language__code=get_language(),
        units__levelsgroup__id=lvsgroup_id).get().name
    levels = '; '.join(['{} [{}]'.format(level.name, units) for level in
        LevelI18N.objects.filter(
            language__code=get_language(),
            level__levels_group__id=lvsgroup_id)])
    return levels
