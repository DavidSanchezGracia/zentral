import logging
from zentral.core.actions.backends.base import BaseAction
from zentral.contrib.inventory.models import Tag, MachineTag

logger = logging.getLogger('zentral.contrib.inventory.actions.machine_tag')


class Action(BaseAction):
    def get_tags(self, event, probe, action_config_d):
        tags = None
        if 'tags' in action_config_d:
            tags = action_config_d['tags']
        elif 'tags_from_event_payload_attr' in action_config_d:
            tags = event.payload.get(action_config_d['tags_from_event_payload_attr'], [])
        if not tags:
            logger.error("No tags or tags_from_event_payload_attr in machine tag action %s of probe %s",
                         self.name, probe.name)
            return
        if isinstance(tags, dict):
            logger.error("tags must be a list of tag id in machine tag action %s of probe %s",
                         self.name, probe.name)
            return
        elif isinstance(tags, list):
            try:
                tags = [int(t) for t in tags]
            except ValueError:
                logger.error("tags must be a list of tag id in machine tag action %s of probe %s",
                             self.name, probe.name)
                return
        elif isinstance(tags, str):
            try:
                tags = [int(tags)]
            except ValueError:
                logger.error("Invalid tags value in machine tag action %s of probe %s",
                             self.name, probe.name)
                return
        elif isinstance(tags, int):
            tags = [tags]
        tags_qs = Tag.objects.filter(pk__in=tags)
        if tags_qs.count() < len(tags):
            logger.error("Some tags could not be found in machine tag action %s of probe %s",
                         self.name, probe.name)
        return tags_qs

    def trigger(self, event, probe, action_config_d):
        msn = event.metadata.machine_serial_number
        tags = self.get_tags(event, probe, action_config_d)
        if not tags:
            return
        for tag in tags:
            action = action_config_d['action']
            if action == 'add':
                MachineTag.objects.get_or_create(serial_number=msn, tag=tag)
            elif action == 'remove':
                MachineTag.objects.filter(serial_number=msn, tag=tag).delete()
            else:
                raise ValueError("Unknown action '%s' in machine tag action %s of probe %s",
                                 action, self.name, probe.name)
