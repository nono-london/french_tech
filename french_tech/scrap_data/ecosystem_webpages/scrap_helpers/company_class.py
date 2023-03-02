from typing import Union, List


class Company:
    """Class that contains company information as displayed by dealroom website"""

    def __init__(self):
        self.name: str = ""  # company name
        self.company_dr_url: str = ""  # company deal room URL
        self.dealroom_signal: Union[int, None] = None
        self.market: List[str] = []
        self.type: List[str] = []
        self.growth: Union[int, None] = None
        self.launch_date: str = ""
        self.valuation: str = ""
        self.funding: str = ""
        self.location: str = ""
        self.last_round: str = ""
        self.number_job_opening: str = ""
        self.job_board: str = ""
        self.status: str = ""
        self.growth_stage: str = ""
        self.web_visits_chg_1Y: Union[int, None] = None
        self.web_employees_chg_1Y: Union[int, None] = None

    def __str__(self):
        """Handles the way the class Company is represented as a String and with the print() function"""
        string_rep: str = f"Company(" \
                          f"name: {self.name}, " \
                          f"company_dr_url: {self.company_dr_url}, " \
                          f"dealroom_signal: {self.dealroom_signal}"

        return string_rep
