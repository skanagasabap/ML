from typing import Dict, Text, List, Optional, Any

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.types import DomainDict

import actions.SMAX_Request_Create as SMAX
from pprint import pprint

# show projects
class ValidateRegisterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_register_form"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        return []

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate slot value."""
        if not slot_value:
         return {"registeremail": None}
        else: 
         return {"registeremail": slot_value}	
class ActionSubmitProject(Action):
    def name(self) -> Text:
        return "action_submitregister"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
	
        user_name = tracker.get_slot("registeremail")
        print("email id  is  : ",user_name) 
        
		
        dispatcher.utter_message(template="utter_details_thanks")
        return[]

class ValidatePrinterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_printer_form"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        return []

    def required_slots(self,tracker:Tracker) -> list:
        required_slots = ["name", "label", "problem"]
        return required_slots

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate slot value."""
        if not slot_value:
         return {"name": None}
        else: 
         return {"name": slot_value}	
    
    def validate_label(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate slot value."""
        if not slot_value:
         return {"label": None}
        else: 
         return {"label": slot_value}
    
    def validate_problem(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate slot value."""
        if not slot_value:
         return {"problem": None}
        else: 
         return {"problem": slot_value}

class ActionSubmitProject(Action):
    def name(self) -> Text:
        return "action_submitprinter"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
	
        printer_name = tracker.get_slot("name")
        problem_desc = tracker.get_slot("label")
        problem_type = tracker.get_slot("problem")
        print("Printer Name  is  : ",printer_name) 
        print("Probelm Description is :",problem_desc)
        print("Problem Category is :", problem_type)


        obj = SMAX.SMAXHandler(
            url="https://xxxxx.xxx.xxx",
            tenent_id="xxxxxxx",
            username="xxxxxx@xydomain.com",
            password="xxxxxxx"
        )

        offering_id = 99999999

        if problem_type == "OutofPaper":
            problem_type_c = "OutofPaper_c"
        elif problem_type == "OutOfInk":
            problem_type_c = "OutOfInk_c"
        else:
            problem_type_c = "PaperJam_c"
        
        user_options = {"PrintName_c":printer_name,"PrintProblem_c":problem_type_c}

        res = obj.create_request(                
            offering_id=offering_id,            
            display_label=problem_desc,
            user_options=user_options
        )

        pprint(res)   


		
        dispatcher.utter_message(template="utter_ack")
        return[]
