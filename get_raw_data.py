import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

class ScrapeSoilData:
    """Scraper class for scraping macro & micro table data from soilhealth4.dac.gov.in
    """
    URL = "https://soilhealth4.dac.gov.in/"
    NUTRIENT_MAP = {
    "N": "Nitrogen",
    "P": "Phosphorus",
    "K": "Potassium",
    "S": "Sulphur",
    "Ca": "Calcium",
    "Mg": "Magnesium",
    "Fe": "Iron",
    "Mn": "Manganese",
    "Zn": "Zinc",
    "Cu": "Copper",
    "B": "Boron",
    "Mo": "Molybdenum",
    "Cl": "Chlorine",
    "Ni": "Nickel",
    "Co": "Cobalt",
    "Si": "Silicon",
    "Na": "Sodium",
    "Al": "Aluminium",
    "Se": "Selenium",
    "V": "Vanadium",
    "I": "Iodine",
    "C": "Carbon",
    "H": "Hydrogen",
    "O": "Oxygen",
    "NO3": "Nitrate",
    "NH4": "Ammonium",
    "PO4": "Phosphate",
    "SO4": "Sulfate",
    "CO3": "Carbonate",
    "HCO3": "Bicarbonate"
    }

    def __init__(self):
        print("Starting Scraper Task!\n")
        self.years = ['2023-24', '2024-25', '2025-26']
        self.session = requests.Session()
        self.soup_maker = lambda response_text: BeautifulSoup(response_text, 'html.parser')
        for year in self.years:
            os.makedirs(os.path.join('data', 'raw', year), exist_ok=True)

    def logger(self, info: str | None = None, status: str | None = None, error: str | None = None):
        logger_data = {
            'info': info,
            'status': status,
            'error': error
            }
        print(logger_data)

    def _create_empty_file(self, path) -> None:
        with open(path, 'w'):
            pass

    def _prep_macro_df(self, json: dict[str, str]) -> pd.DataFrame:
        get_high = lambda dictionary,  mac_nutri: dictionary.get(mac_nutri).get('High')
        get_medium = lambda dictionary,  mac_nutri: dictionary.get(mac_nutri).get('Medium')
        get_low = lambda dictionary,  mac_nutri: dictionary.get(mac_nutri).get('Low')
        data = json
        main_dict = {}
        for datum in data:
            village = datum.get('village').get('name')
            main_dict.setdefault('village', []).append(village)
            results: dict = datum.get('results')
            for nutri_key, nutri_dict in results.items():
                nutri_key: str = nutri_key
                nutri_dict: dict = nutri_dict
                if nutri_key.casefold() == 'ph'.casefold():
                    main_dict.setdefault('pH Alkaline', []).append(results.get('pH').get('Alkaline'))
                    main_dict.setdefault('pH Acidic', []).append(results.get('pH').get('Acidic'))
                    main_dict.setdefault('pH Neutral', []).append(results.get('pH').get('Neutral'))
                elif list(nutri_dict.keys()) == ['High', 'Low', 'Medium']:
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} High", []).append(get_high(results, nutri_key))
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Medium", []).append(get_medium(results, nutri_key))
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Low", []).append(get_low(results, nutri_key))
                elif list(nutri_dict.keys()) == ['Sufficient', 'Deficient']:
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Sufficient", []).append(results.get(nutri_key).get('Sufficient'))
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Deficient", []).append(results.get(nutri_key).get('Deficient'))
        return pd.DataFrame(main_dict)

    def _prep_micro_df(self, json: dict[str, str]) -> pd.DataFrame:
        get_high = lambda dictionary,  mac_nutri: dictionary.get(mac_nutri).get('High')
        get_medium = lambda dictionary,  mac_nutri: dictionary.get(mac_nutri).get('Medium')
        get_low = lambda dictionary,  mac_nutri: dictionary.get(mac_nutri).get('Low')
        data = json
        main_dict = {}
        for datum in data:
            village = datum.get('village').get('name')
            main_dict.setdefault('village', []).append(village)
            results: dict = datum.get('results')
            for nutri_key, nutri_dict in results.items():
                nutri_dict: dict = nutri_dict
                if nutri_key.casefold() == 'ph'.casefold():
                    main_dict.setdefault('pH Alkaline', []).append(results.get('pH').get('Alkaline'))
                    main_dict.setdefault('pH Acidic', []).append(results.get('pH').get('Acidic'))
                    main_dict.setdefault('pH Neutral', []).append(results.get('pH').get('Neutral'))
                elif list(nutri_dict.keys()) == ['High', 'Low', 'Medium']:
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} High", []).append(get_high(results, nutri_key))
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Medium", []).append(get_medium(results, nutri_key))
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Low", []).append(get_low(results, nutri_key))
                elif list(nutri_dict.keys()) == ['Sufficient', 'Deficient']:
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Sufficient", []).append(results.get(nutri_key).get('Sufficient'))
                    main_dict.setdefault(f"{self.NUTRIENT_MAP.get(nutri_key.capitalize())} Deficient", []).append(results.get(nutri_key).get('Deficient'))
                elif list(nutri_dict.keys()) == ['Saline', 'NonSaline']:
                    main_dict.setdefault(f"{nutri_key} Saline", []).append(results.get(nutri_key).get('Saline'))
                    main_dict.setdefault(f"{nutri_key} NonSaline", []).append(results.get(nutri_key).get('NonSaline'))
        return pd.DataFrame(main_dict)

    def _make_request_for_macro_data(self, year: str, state_id: str, district_id: str, block_id: str) -> dict:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://soilhealth.dac.gov.in",
            "priority": "u=1, i",
            "referer": "https://soilhealth.dac.gov.in/",
            "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        payload = {
            "query": """
                query GetNutrientDashboardForPortal(
                $state: ID
                $district: ID
                $block: ID
                $village: ID
                $cycle: String
                $count: Boolean
                ) {
                getNutrientDashboardForPortal(
                    state: $state
                    district: $district
                    block: $block
                    village: $village
                    cycle: $cycle
                    count: $count
                )
                }
            """,
            "variables": {
                "cycle": year,
                "state": state_id,
                "district": district_id,
                "block": block_id
            }
        }
        response = requests.post(self.URL, headers=headers, json=payload)
        return response.json()

    def _make_request_for_micro_data(self, year: str, state_id: str, district_id: str, block_id: str) -> dict:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://soilhealth.dac.gov.in",
            "priority": "u=1, i",
            "referer": "https://soilhealth.dac.gov.in/",
            "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        data = {
            "query": """
                    query GetNutrientDashboardForPortal(
                    $state: ID
                    $district: ID
                    $block: ID
                    $village: ID
                    $cycle: String
                    $count: Boolean
                    ) {
                    getNutrientDashboardForPortal(
                        state: $state
                        district: $district
                        block: $block
                        village: $village
                        cycle: $cycle
                        count: $count
                    )
                    }
            """,
            "variables": {
                "cycle": year,
                "state": state_id,
                "district": district_id,
                "block": block_id
            }
        }
        response = requests.post(self.URL, headers=headers, json=data)
        return response.json()

    def _encoded_values_for_state(self) -> dict:
        response_dict = self._get_all_states()
        states = {i.get('name'): i.get('_id') for i in response_dict.get('data').get('getState')}
        self.states = states
        return states
        
    def _encoded_values_for_district_by_state(self, state_name: str) -> dict:
        state_id = self.states.get(state_name)
        response_dict = self._get_all_district_for_a_state(state_id=state_id)
        district_dict = {i.get('name'): i.get('_id') for i in response_dict.get('data').get('getdistrictAndSubdistrictBystate')}
        self.districts = district_dict
        return district_dict
    
    def _encoded_values_for_block_by_district(self, district_name: str) -> dict:
        district_id = self.districts.get(district_name)
        response_dict = self._get_all_blocks_for_a_district(district_id)
        block_dict = {i.get('name'): i.get('_id') for i in response_dict.get('data').get('getBlocks')}
        self.block_dicts = block_dict
        return block_dict
     
    def _get_all_blocks_for_a_district(self, district_id: str):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://soilhealth.dac.gov.in",
            "priority": "u=1, i",
            "referer": "https://soilhealth.dac.gov.in/",
            "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        payload = {
            "query": """
                    query Query($district: ID) {
                        getBlocks(district: $district)
                    }
            """,
            "variables": {
                "district": district_id
            }
        }
        response = requests.post(self.URL, headers=headers, json=payload)
        return response.json()

    def _get_all_district_for_a_state(self, state_id: str):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://soilhealth.dac.gov.in",
            "priority": "u=1, i",
            "referer": "https://soilhealth.dac.gov.in/",
            "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        payload = {
            "query": """
                    query GetdistrictAndSubdistrictBystate($state: ID!, $subdistrict: Boolean) {
                        getdistrictAndSubdistrictBystate(state: $state, subdistrict: $subdistrict)
                    }
                    """,
            "variables": {
                "state": state_id,
                "subdistrict": None
            }
        }
        response = self.session.post(self.URL, headers=headers, json=payload)
        return response.json()

    def _get_all_states(self) -> str:

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://soilhealth.dac.gov.in",
            "priority": "u=1, i",
            "referer": "https://soilhealth.dac.gov.in/",
            "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        payload = {
            "query": """
                    query GetState($getStateId: String) {
                        getState(id: $getStateId)
                    }
                    """
        }
        response = requests.post(self.URL, headers=headers, json=payload)
        return response.json()

    def _process_block(self, year, state, district, block):
        
        try:
            state_id = self.states.get(state)
            district_id = self.states.get(district)
            block_id = self.block_dicts.get(block)
            self.logger(f"Working on {year}-{state}-{district}-{block}")
            if os.path.exists(os.path.join('data', 'raw', year, state, district, f"{block}_macro.csv")):
                self.logger(info="Block macro file already exists")
            else:
                main_request_macro_json = self._make_request_for_macro_data(year=year, state_id=state_id, district_id=district_id, block_id=block_id)
                self.process_macro_data(main_request_macro_json, year, state, district, block)
            if os.path.exists(os.path.join('data', 'raw', year, state, district, f"{block}_micro.csv")):
                self.logger(info="Block micro file already exists")
            else:
                main_request_micro_json = self._make_request_for_micro_data(year, state_id, district_id, block_id)
                self.process_micro_data(main_request_micro_json, year, state, district, block)
            self.logger(status=f"Done with {year}-{state}-{district}-{block}")
        except Exception as e:
            self.logger(status="Skipping error received to continue scraping rest of the data", error=e)

    def execute(self) -> None:
        states = self._encoded_values_for_state()
        for year in self.years:
            try:
                for state in states:
                    try: 
                        districts = self._encoded_values_for_district_by_state(state)
                        try:
                            for district in districts:
                                blocks = self._encoded_values_for_block_by_district(district)
                                try:
                                    with ThreadPoolExecutor(max_workers=10) as executor:
                                        futures = [executor.submit(self._process_block, year, state, district, block) for block in blocks]
                                        for _ in as_completed(futures):
                                            pass
                                    self.logger(status=f"Done with {year}-{state}-{district}")
                                except Exception as e:
                                    self.logger(status="Skipping error received to continue scraping rest of the data", error=e)
                        except Exception as e:
                            self.logger(status="Skipping error received to continue scraping rest of the data", error=e)
                    except Exception as e:
                        self.logger(status="Skipping error received to continue scraping rest of the data", error=e)
                self.logger(status=f"Done with {year}-{state}")
            except Exception as e:
                self.logger(status="Skipping error received to continue scraping rest of the data", error=e)
            self.logger(status=f"Done with {year}-{state}")

    def process_macro_data(self, json_response: dict, year: str, state: str, district: str, block: str) -> None:
        block = block.strip()
        data = json_response.get('data').get('getNutrientDashboardForPortal')
        if data == []:
            os.makedirs(os.path.join('data', 'raw', year, state, district), exist_ok=True)
            self._create_empty_file(os.path.join('data', 'raw',  year, state, district, f'no_rows_for_{block}_macro.txt'))
            self._create_empty_file(os.path.join('data', 'raw',  year, state, district, f'{block}_macro.csv'))
        else:
            dataFrame = self._prep_macro_df(data)
            os.makedirs(os.path.join('data', 'raw', year, state, district), exist_ok=True)
            dataFrame.to_csv(os.path.join('data', 'raw', year, state, district, f'{block}_macro.csv'), index=False)

    def process_micro_data(self, json_response: dict, year: str, state: str, district: str, block: str) -> None:
        block = block.strip()
        data = json_response.get('data').get('getNutrientDashboardForPortal')
        if data == []:
            os.makedirs(os.path.join('data', 'raw', year, state, district), exist_ok=True)
            self._create_empty_file(os.path.join('data', 'raw',  year, state, district, f'no_rows_for_{block}_micro.txt'))
            self._create_empty_file(os.path.join('data', 'raw',  year, state, district, f'{block}_micro.csv'))
        else:
            dataFrame = self._prep_micro_df(data)
            os.makedirs(os.path.join('data', 'raw', year, state, district), exist_ok=True)
            dataFrame.to_csv(os.path.join('data', 'raw', year, state, district, f'{block}_micro.csv'), index=False)

if __name__ == "__main__":
    runner = ScrapeSoilData()
    runner.execute()
