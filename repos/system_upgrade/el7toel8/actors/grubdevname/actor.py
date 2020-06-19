from leapp.actors import Actor
from leapp.libraries.actor.grubdevname import get_grub_device
from leapp.libraries.common.config import architecture
from leapp.models import GrubDevice
from leapp.tags import FactsPhaseTag, IPUWorkflowTag


class Grubdevname(Actor):
    """
    Get name of block device where GRUB is located
    """

    name = 'grubdevname'
    consumes = ()
    produces = (GrubDevice,)
    tags = (FactsPhaseTag, IPUWorkflowTag)

    def process(self):
        if architecture.matches_architecture(architecture.ARCH_S390X):
            return
        get_grub_device()
