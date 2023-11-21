from collections import defaultdict


class ActiveCookieExtractor:
    """
    A class used to extract most active cookie in target date
    ...

    Attributes
    ----------
    cookie_dict : dict
        a dictionary to track count of each cookies. 
        Each date will hold dictionary with key of cookie and value of count.
    count_dict : dict
        a dictionary to track cookies of each count.
        Each date will hold dictionary with key of count and value of set of cookies.
    cookie_list : list
        list of (cookie, date)
    target_date : datetime
        target date to find active cookie

    Methods
    -------
    _initiate_dictionary()
        Initiates count_dict and cookie_dict

    extract_active_cookies()
        return list of most active cookies in target date.
    """
    def __init__(self, cookie_list, target_date):
        self.cookie_dict = defaultdict(dict)
        self.count_dict = defaultdict(int)
        self.cookie_list = cookie_list
        self.target_date = target_date
        self.initiate_dictionary()

    def initiate_dictionary(self):
        """
        We will iterate through cookie and date inside cookie list.
        Then, we will update cookie_dict with new count.
        Based on the new count, we will remove old count in count_dict, 
        and add cookie to new count
        """
        for cookie, date in self.cookie_list:
            # Update cookie_dict
            cookie_dict_date = self.cookie_dict.setdefault(date, defaultdict(int))
            cookie_dict_date[cookie] += 1

            # Update count_dict
            count = cookie_dict_date[cookie]
            count_dict_date = self.count_dict.setdefault(date, defaultdict(set))
            count_dict_date[count].add(cookie)

            # Adjust for count greater than 1
            if count > 1:
                count_dict_date[count - 1].discard(cookie)

    def extract_active_cookies(self):
        """
        Based on the count of the target date, we will get maximum among count.
        Then, we will get list of active cookies with that count and date. 
        :return: list of cookies
        """
        count_in_date = self.count_dict.get(self.target_date, {})
        most_active_cookies = count_in_date.get(max(count_in_date, default=0), set())
        return list(most_active_cookies)
