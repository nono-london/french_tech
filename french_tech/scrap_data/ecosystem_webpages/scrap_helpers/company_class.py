from typing import Union, List


class Company:
    """Class that contains company information as displayed by dealroom website"""

    def __init__(self):
        self.name: str = ""  # company name
        self.company_dr_url: str = ""  # company deal room URL
        self.company_url: str = ""  # company URL
        self.dealroom_signal: Union[int, None] = None
        self.market: List[str] = []
        self.type: List[str] = []

        self.growth: str = ""  # based on number of employees
        self.number_of_employees: str = ""  # Number of employees
        self.launch_date: str = ""
        self.valuation: str = ""
        self.funding: str = ""

        self.location: str = ""
        self.last_round: str = ""
        self.number_job_opening: str = ""
        self.job_board: str = ""
        self.revenue: Union[str, None] = None

        self.status: str = ""
        self.growth_stage: str = ""
        self.web_visits_chg_1Y: Union[int, None] = None
        self.web_employees_chg_1Y: Union[int, None] = None
        self.enterprise_value: Union[str, None] = None

        self.twitter_url: Union[str, None] = None
        self.linkedin_url: Union[str, None] = None
        self.facebook_url: Union[str, None] = None

    def __str__(self):
        """Handles the way the class Company is represented as a String and with the print() function"""
        string_rep: str = f"Company(" \
                          f"name: {self.name}, " \
                          f"company_dr_url: {self.company_dr_url}, " \
                          f"company_url: {self.company_url}, " \
                          f"dealroom_signal: {self.dealroom_signal}, " \
                          f"market: {self.market}, " \
                          f"type: {self.type}, " \
                          f"growth: {self.growth}, " \
                          f"employees: {self.number_of_employees}, " \
                          f"launch_date: {self.launch_date}, " \
                          f"valuation: {self.valuation}, " \
                          f"funding: {self.funding}, " \
                          f"hqLocations: {self.location}, " \
                          f"last_round: {self.last_round}, " \
                          f"number_job_opening: {self.number_job_opening}, " \
                          f"job_board: {self.job_board}, " \
                          f"revenue: {self.revenue}, " \
                          f"growth_stage: {self.growth_stage}, " \
                          f"web_visits_chg_1Y: {self.web_visits_chg_1Y}, " \
                          f"web_employees_chg_1Y: {self.web_employees_chg_1Y}, " \
                          f"enterprise_value: {self.enterprise_value}, " \
                          f"twitter_url: {self.twitter_url}, " \
                          f"linkedin_url: {self.linkedin_url}, " \
                          f"facebook_url: {self.facebook_url}, " \
                          f")"

        return string_rep

    def __hash__(self):
        return hash(self.company_dr_url)

    def __eq__(self, other):
        is_company: bool = isinstance(other, self.__class__)

        if not is_company:
            return False

        # what to do in that case?
        # should unsure that is never True
        if self.company_dr_url == "" and other.company_dr_url == "":
            return False

        return self.company_dr_url == other.company_dr_url


if __name__ == '__main__':
    my_company = Company()
    my_company.market = ['aksj', 'asalsk']
    my_company.market = [element for element in my_company.market]
    # print(my_company)
    print(hash("iuiu"))
    print(vars(my_company))
