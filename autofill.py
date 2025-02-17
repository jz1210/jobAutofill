from DrissionPage import ChromiumPage
import json

class JobApplicationAutofiller:
    def __init__(self, config_path: str = 'user_data.json'):
        # Connect to existing browser session
        self.page = ChromiumPage(addr_or_opts='127.0.0.1:9222')
        
        # Load user data
        with open(config_path) as f:
            self.user_data = json.load(f)
        
        # State abbreviation standardization
        # self.user_data['address']['state'] = self.user_data['address']['state'].upper()

    def _fill_current_page(self):
        try:
            # Personal Information
            # Get all elements whose id attribute contains first name
            fnames = self.page.eles('@id:firstName')
            for fname in fnames:
                fname.input(self.user_data['first_name'])
            
            # Get all elements whose id attribute contains last name
            lnames = self.page.eles('@id:lastName')
            for lname in lnames:
                lname.input(self.user_data['last_name'])

            print("Form filled successfully")
            
        except Exception as e:
            print(f"Error: {str(e)}")

    def _handle_address(self):
        # Autofill the address
        self.page.ele('@id:addressLine1').input(self.user_data['address']['street'])
        self.page.ele('@id:city').input(self.user_data['address']['city'])
        self.page.ele('@|id:Region@|id:state@|id:State@|id:region').click()
        self.page.ele(f'text:{self.user_data['address']['state']}', timeout=5).click()
        self.page.ele('@|id:zipCode@|id:postalCode').input(self.user_data['address']['zip_code'])

    def _fill_phone_number(self):
        # Autofill the phone number
        pnumber = self.page.eles('@|id:phone@|id:phoneNumber')
        for phone in pnumber:
            phone.input(self.user_data['phone'])

    def apply_to_current_page(self):
        """Execute form filling on current browser tab"""
        self._fill_current_page()
        self._handle_address()
        self._fill_phone_number()

if __name__ == "__main__":
    # Connect to existing browser and apply
    applicator = JobApplicationAutofiller()
    applicator.apply_to_current_page()
