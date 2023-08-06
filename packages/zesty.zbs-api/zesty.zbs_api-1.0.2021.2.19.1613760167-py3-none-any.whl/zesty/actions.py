"""
Command Design Pattern (Behavioral Design Pattern)
"""
import uuid as uuid_gen
from typing import Dict
from zesty.models.hf_interface import *
from zesty.models.hf_interface import *
from zesty.models.disk_mon import FileSystem


class ZBSActionData:
    mount_path = None
    device = None
    filesystem = None
    fs_type = None
    is_partition = False
    partition_number = None
    LV = None
    VG = None
    lvm_path = None
    chunk_size = None

    def __init__(self, mount_path=None,
                 device=None,
                 filesystem=None,
                 fs_type=None,
                 is_partition=False,
                 partition_number=None,
                 LV=None,
                 VG=None,
                 lvm_path=None,
                 chunk_size=None):
        self.mount_path = mount_path
        self.filesystem = filesystem
        self.fs_type = fs_type
        self.device = device
        self.is_partition = is_partition
        self.partition_number = partition_number
        self.LV = LV
        self.VG = VG
        self.lvm_path = lvm_path
        self.chunk_size = chunk_size

    def serialize(self):
        return self.__dict__

    def set_data(self, json):
        self.mount_path = json.get('mount_path')
        self.filesystem = json.get('filesystem')
        self.fs_type = json.get('fs_type')
        self.device = json.get('device')
        self.is_partition = json.get('is_partition', False)
        self.partition_number = json.get('partition_number', '')
        self.LV = json.get('LV', '')
        self.VG = json.get('VG', '')
        self.lvm_path = json.get('lvm_path', '')
        self.chunk_size = json.get('chunk_size', 0)

        return self


class ZBSAgentReceiver:
    """
    The ZBSAgentReceiver (Receiver class in the Command pattern) contain some important business logic.
    It knows how to perform any kind of action sent by the ZBS Backend.
    ZBSAgent is an abstract class, while the concrete implementations should be per OS
    """

    @abstractmethod
    def do_nothing(self, data: ZBSActionData) -> None:
        raise NotImplementedError(
            "ZBSAgentReceiver 'do_nothing' is abstract, please implement a concrete per OD receiver")

    @abstractmethod
    def extend_fs(self, data: ZBSActionData, action_id) -> None:
        raise NotImplementedError(
            "ZBSAgentReceiver 'extend_fs' is abstract, please implement a concrete per OD receiver")

    @abstractmethod
    def add_disk(self, data: ZBSActionData, action_id) -> None:
        raise NotImplementedError(
            "ZBSAgentReceiver 'add_disk' is abstract, please implement a concrete per OD receiver")

    @abstractmethod
    def balance_fs(self, data: ZBSActionData, action_id) -> None:
        raise NotImplementedError(
            "ZBSAgentReceiver 'balance_fs' is abstract, please implement a concrete per OD receiver")

    @abstractmethod
    def remove_disk(self, data: ZBSActionData, action_id) -> None:
        raise NotImplementedError(
            "ZBSAgentReceiver 'remove_disk' is abstract, please implement a concrete per OD receiver")

    @abstractmethod
    def balance_ebs_structure(self, data: ZBSActionData, action_id) -> None:
        raise NotImplementedError(
            "ZBSAgentReceiver 'balance_ebs_structure' is abstract, please implement a concrete per OD receiver")


class SpecialInstructions(ISpecialInstructions):
    """
    Constructor for special instructions with optional parameters:
    * dev_id: identify the device for the filesystem to which the action is attached
    * size: specify the capacity for a new device or the additional capacity when extending a device
    * sub_actions: when an action implements multiple actions, specify a dictionary:
        -- { int(specifies action priorities): list(actions that can be run in parallel) }
        -- Actions in a list keyed to a higher order cannot start until all Actions of lower orders complete
    """

    def __init__(self, dev_id: str = None, size: int = None, sub_actions: Dict[int, Dict[str, IActionHF]] = None):
        self.dev_id = dev_id
        self.size = size
        self.sub_actions = sub_actions


class ZBSAction(IActionHF):
    """
    Base command class
    Delegates the business logic to the receiver
    There are receivers per OS (Linux and Windows for now)
    """
    TYPE_FIELD_NAME = "type"
    DATA_FIELD_NAME = "data"
    STATUS_FIELD_NAME = "status"
    UUID_FIELD_NAME = "uuid"
    SPECIAL_INSTRUCTIONS_FIELD_NAME = "_ZBSAction__special_instructions"

    __uuid = None
    __status: IActionHF.Status = IActionHF.Status.NEW
    __special_instructions: SpecialInstructions

    def __init__(self, receiver: ZBSAgentReceiver = None, data: ZBSActionData = None, uuid: str = None):
        self.receiver = receiver
        self.data = data

        if uuid is not None:
            self.__uuid = uuid
        else:
            self.__uuid = str(uuid_gen.uuid4())

    def __repr__(self):
        return "<Action Type: {} | Action Status: {} | SpecialInstructions: {}>".format(self.get_action_type(), self.get_status(), self.get_special_instructions().__dict__)

    def set_data(self, data: ZBSActionData):
        self.data = data

    def set_receiver(self, receiver: ZBSAgentReceiver):
        self.receiver = receiver

    def serialize(self):
        result = self.__dict__
        result[ZBSAction.TYPE_FIELD_NAME] = self.get_action_type()
        result[ZBSAction.DATA_FIELD_NAME] = self.data.serialize() if self.data is not None else None
        result[ZBSAction.STATUS_FIELD_NAME] = self.get_status().name
        result[ZBSAction.UUID_FIELD_NAME] = self.get_action_id()
        if hasattr(self, '_ZBSAction__special_instructions'):
            result[
                ZBSAction.SPECIAL_INSTRUCTIONS_FIELD_NAME] = self.get_special_instructions().__dict__ if self.__special_instructions is not None else None

        return result

    # ActionHF interface implementation
    def get_action_id(self) -> str:
        return self.__uuid

    def get_action_type(self) -> str:
        return str(type(self).__name__)

    def get_status(self) -> IActionHF.Status:
        return self.__status

    def set_status(self, status: IActionHF.Status):
        self.__status = status

    def get_special_instructions(self) -> SpecialInstructions:
        return self.__special_instructions

    def set_special_instructions(self, special_instructions: SpecialInstructions):
        self.__special_instructions = special_instructions

    @staticmethod
    def deserialize_type(json):
        return json[ZBSAction.TYPE_FIELD_NAME]

    @staticmethod
    def deserialize_data(json):
        return ZBSActionData().set_data(json[ZBSAction.DATA_FIELD_NAME])

    @staticmethod
    def deserialize_uuid(serialized_action):
        return serialized_action.get(ZBSAction.UUID_FIELD_NAME)

    @staticmethod
    def deserialize_status(serialized_action):
        return serialized_action.get(ZBSAction.STATUS_FIELD_NAME)

    @staticmethod
    def deserialize_special_instructions(serialized_action):
        if not isinstance(serialized_action, dict):
            serialized_action = serialized_action.serialize()
        special_instructions = SpecialInstructions(
            dev_id=serialized_action.get(ZBSAction.SPECIAL_INSTRUCTIONS_FIELD_NAME, {}).get('dev_id'),
            size=serialized_action.get(ZBSAction.SPECIAL_INSTRUCTIONS_FIELD_NAME, {}).get('size'),
            sub_actions=serialized_action.get(ZBSAction.SPECIAL_INSTRUCTIONS_FIELD_NAME, {}).get('sub_actions'),
        )
        for key, val in serialized_action.get(ZBSAction.SPECIAL_INSTRUCTIONS_FIELD_NAME, {}).items():
            if key not in ['dev_id', 'size', 'sub_actions']:
                exec('special_instructions.' + key + '=val')

        return special_instructions

    @staticmethod
    def deserialize_action(serialized_action):
        action_type = ZBSAction.deserialize_type(serialized_action)
        action_data = ZBSAction.deserialize_data(serialized_action) if serialized_action.get(
            ZBSAction.DATA_FIELD_NAME) is not None else None
        action_uuid = ZBSAction.deserialize_uuid(serialized_action)
        action_status = ZBSAction.deserialize_status(serialized_action)

        action_to_perform = ZBSActionFactory.create_action(action_type, action_uuid)
        action_to_perform.set_data(action_data)
        action_to_perform.set_status(IActionHF.Status[serialized_action.get('status')])
        if ZBSAction.SPECIAL_INSTRUCTIONS_FIELD_NAME in serialized_action:
            special_instructions = ZBSAction.deserialize_special_instructions(serialized_action)
            action_to_perform.set_special_instructions(special_instructions)

        return action_to_perform

    @abstractmethod
    def execute(self):
        raise NotImplementedError("BaseAction is abstract, please implement a concrete action")


class FileSystemHF(IFileSystemHF):
    def __init__(self, fs_id: str, fs_usage: int, devices: Dict[str, FileSystem.BlockDevice], existing_actions: Dict[str, ZBSAction]):
        self.fs_id = fs_id
        self.fs_usage = fs_usage
        self.devices = devices
        self.existing_actions = existing_actions

    def get_fs_id(self) -> str:
        return self.fs_id

    def get_usage(self) -> int:
        return self.fs_usage

    def get_devices(self) -> Dict[str, FileSystem.BlockDevice]:
        return self.devices

    def get_existing_actions(self) -> Dict[str, ZBSAction]:
        return self.existing_actions


class DoNothingAction(ZBSAction):
    """
    Do nothing action
    """

    def execute(self):
        print("Do nothing || Action ID : {}".format(self.get_action_id()))

    class Factory:
        def create(self, uuid): return DoNothingAction(uuid=uuid)


class ExtendFileSystemAction(ZBSAction):
    """
    Extend File System Action.
    """

    def execute(self, fs):
        try:
            return self.receiver.extend_fs(self.get_special_instructions(), self.get_action_id(), fs)
        except AttributeError as ex:
            print("Failed to execute command '{}': error is '{}'".format(self.get_action_type(), ex))

    class Factory:
        def create(self, uuid): return ExtendFileSystemAction(uuid=uuid)


class AddDiskAction(ZBSAction):
    """
    Add Disk Action.
    """

    def execute(self, fs):
        try:
            return self.receiver.add_disk(self.get_special_instructions(), self.get_action_id(), fs)
        except AttributeError as ex:
            print("Failed to execute command '{}': error is '{}'".format(self.get_action_type(), ex))

    class Factory:
        def create(self, uuid): return AddDiskAction(uuid=uuid)


class RemoveDiskAction(ZBSAction):
    """
    Remove Disk Action.
    """

    def execute(self, fs):
        try:
            return self.receiver.remove_disk(self.get_special_instructions(), self.get_action_id(), fs)
        except AttributeError as ex:
            print("Failed to execute command '{}': error is '{}'".format(self.get_action_type(), ex))

    class Factory:
        def create(self, uuid): return RemoveDiskAction(uuid=uuid)


class BalanceFileSystemAction(ZBSAction):
    """
    Balance File System Action.
    """

    def execute(self):
        try:
            self.receiver.balance_fs(self.data, self.get_action_id())
        except AttributeError as ex:
            print("Failed to execute command '{}': error is '{}'".format(self.get_action_type(), ex))

    class Factory:
        def create(self, uuid): return BalanceFileSystemAction(uuid=uuid)


class BalanceEBSStructureAction(ZBSAction):
    """
    Balance EBS structure Action.
    """

    def execute(self):
        try:
            self.receiver.extend_fs(self.data, self.get_action_id())
            self.receiver.remove_disk(self.data, self.get_action_id())
        except AttributeError as ex:
            print("Failed to execute command '{}': error is '{}'".format(self.get_action_type(), ex))

    class Factory:
        def create(self, uuid): return BalanceEBSStructureAction(uuid=uuid)


class ZBSActionFactory:
    actions = {}

    def create_action(action_type, uuid=None):
        if action_type not in ZBSActionFactory.actions:
            ZBSActionFactory.actions[action_type] = eval(action_type + '.Factory()')
        return ZBSActionFactory.actions[action_type].create(uuid)

    create_action = staticmethod(create_action)
