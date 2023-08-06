from typing import List, Dict, Any, Union


class Interface():
    def __init__(self, **kwargs):
        pass

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Text(Interface):
    def __init__(self, mutations: Union[str, Dict[str, str]]):
        if isinstance(mutations, str):
            self.mutations = {"original": mutations}
        else:
            self.mutations = mutations

    def add_mutation(self, key, mutation):
        self.mutations[key] = mutation

    def get(self, key="original") -> str:
        return self.mutations.get(key, "")

    def to_dict(self):
        return self.mutations

    def get_keys(self):
        return [k for k in self.mutations]

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Entity(Interface):
    def __init__(self, name: str, input_type: str, val: str, sidx: int, eidx: int, confidence: float) -> None:
        self.name = name
        self.input_type = input_type
        self.val = val
        self.sidx = sidx
        self.eidx = eidx
        self.confidence = confidence

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Intent(Interface):
    def __init__(self, chosen: str, scores: Dict[str, float]) -> None:
        self.chosen = chosen
        self.scores = scores

    def is_intent_chosen(self):
        return self.chosen is not None

    def confidence(self):
        return self.scores[self.chosen]

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Misc(Interface):
    def __init__(self,
                 buttons: List[str] = None,
                 multiselects: List[str] = None,
                 checkboxes: List[str] = None,
                 date: str = None,
                 file: str = None,
                 latitude: str = None,
                 longitude: str = None,
                 nfc: Any = None,
                 form: List[Any] = None
                 ):
        self.buttons = buttons
        self.multiselects = multiselects
        self.checkboxes = checkboxes
        self.date = date
        self.file = file
        self.latitude = latitude
        self.longitude = longitude
        self.nfc = nfc
        self.form = form

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class UserMessage(Interface):
    def __init__(self,
                 user_id: str = None,
                 text: Text = None,
                 misc: Misc = None,
                 intent: Intent = None,
                 entities: List[Entity] = None):
        self.user_id = user_id
        self.text = text
        self.misc = misc
        self.intent = intent
        self.entities = entities

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "text": self.text.to_dict() if self.text is not None else None,
            "misc": self.misc.to_dict() if self.text is not None else None,
            "intent": self.intent.to_dict() if self.text is not None else None,
            "entities": [e.to_dict() for e in self.entities] if self.entities is not None else None
        }

    @classmethod
    def from_dict(cls, message_dict):
        def is_exist(key, null=None):
            return key in message_dict and message_dict[key] is not null

        obj = cls()
        obj.user_id = message_dict["user_id"]
        obj.text = Text(message_dict["text"]) if is_exist("text") else None
        obj.misc = Misc(**message_dict["misc"]) if is_exist("misc") else None
        obj.intent = Intent.from_dict(
            message_dict["intent"]) if is_exist("intent") else None
        obj.entities = [Entity.from_dict(
            e) for e in message_dict["entities"]] if is_exist("entities", []) else []
        return obj


class ActorMessage(Interface):
    def __init__(self,
                 user_id: str = None,
                 code: str = None,
                 text: str = None,
                 list: List[str] = None,
                 buttons: List[str] = None,
                 checkboxes: List[str] = None,
                 multiselects: List[str] = None,
                 images: List[str] = None,
                 files: List[str] = None):
        self.user_id = user_id
        self.code = code
        self.text = text
        self.buttons = buttons
        self.checkboxes = checkboxes
        self.multiselects = multiselects
        self.images = images
        self.files = files
        self.list = list

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


class Command:
    class Do(Interface):
        def __init__(self, action: str, request: UserMessage) -> None:
            self.name = "do"
            self.action = action
            self.request = request

        def app(self):
            return self.action.split(":")[0]

        def action_name(self):
            return self.action.split(":")[1]

        def to_dict(self):
            return {
                "name": "do",
                "action": self.action,
                "request": self.request.to_dict()
            }

        @classmethod
        def from_dict(cls, dict):
            return {
                "name": "do",
                "action": dict["action"],
                "request": UserMessage(dict["request"])
            }

    class Say(Interface):
        def __init__(self, msg: ActorMessage):
            self.name = "say"
            self.msg = msg

        def to_dict(self):
            return {
                "name": "do",
                "msg": self.msg.to_dict()
            }

        @classmethod
        def from_dict(cls, dict):
            return {
                "name": "do",
                "msg": ActorMessage(dict["msg"])
            }

    class Rerun(Interface):
        def __init__(self):
            self.name = "rerun"

        @classmethod
        def from_dict(cls, dict):
            return cls(**dict)

    @staticmethod
    def publish_commands(commands: List[Interface]):
        return [c.to_dict() for c in commands]

    @staticmethod
    def decode_commands(commands: List[Dict[str, Any]]):
        c = []
        for command in commands:
            if command["name"] == "do":
                c.append(Command.Do.from_dict(command))
            elif command["name"] == "say":
                c.append(Command.Say.from_dict(command))
            elif command["name"] == "rerun":
                c.append(Command.Rerun.from_dict(command))
            else:
                raise ValueError("command not supported")
        return c


class ActorResponse(Interface):
    def __init__(self,
                 actor: str = None,
                 user_id: str = None,
                 variables: Dict[str, Any] = None,
                 request: str = None,
                 user_message: UserMessage = None):
        self.actor = actor
        self.user_id = user_id
        self.variables = variables
        self.request = request
        self.user_message = user_message

    @classmethod
    def from_dict(cls, response_dict):
        obj = cls()
        obj.actor = response_dict.get("actor", None)
        obj.user_id = response_dict.get("user_id", None)
        obj.variables = response_dict.get("variables", None)
        obj.request = response_dict.get("request", None)
        if "user_message" in response_dict and response_dict["user_message"] is not None:
            obj.user_message = UserMessage(response_dict["user_message"])
        else:
            obj.user_message = None
        return obj

    def to_dict(self):
        return {
            "actor": self.actor,
            "user_id": self.user_id,
            "variabels": self.variables,
            "request": self.request,
            "user_message": self.user_message.to_dict() if self.user_message is not None else None
        }
