import os
from .Manager import *

class MessageManager(Manager):

   def __init__(self):
      super().__init__()
      self.contents = {"runtime": {}, "memory": {}}
      self.results = {"runtime": {}, "memory": {}}
      self.message_content = ""

   def get_test_names(self, data):
         """Create a set containing all test names by extracting the tests (keys) from the data
         Returns:
            all_tests: Set of all test names
         """
         all_tests = set()
         for data_by_machine in data.values():
            all_tests.update(data_by_machine.keys())
         
         return all_tests

   def organize_data_by_test(self, data):
         """Creates new runtime/memory dictionaries that use test name as key and have data for each machine 
         under each test. 
         Returns:
            results (dict): Pass/fail data for each test and machine. Primary key is test. Secondary key is machine:
               {'datm_cdeps_ciceC_cfsr_intel': 
                  {'acorn': {'cb16f329': 188, 'ead2c35f': 188, ...}
                  'gaeac6': {'cb16f329': 119, 'ead2c35f': 120, ...}}
               }
         """

         tests = self.get_test_names(data)

         results = {}

         for test in tests:
            for machine, test_data in data.items():
               if test not in test_data:
                  continue # No data to add
               else:
                  results.setdefault(test, {}).update({machine: test_data[test]})
                  #results[test].setdefault(machine, []).update()
                  
         return results

   def create_message_content(self, data, category):
      """If there are tests whose runtime/memory results are 2 standard deviations above the mean for 3+ tests, 
      append this information to self.message_content.
      """
      fail = '❌'
      self.results[category] = self.organize_data_by_test(data)

      matching = {}
      for test, result in self.results[category].items(): 
         for machine, is_fail in result.items():
            if is_fail == fail:
               matching.setdefault(test, []).append(machine)

      if not matching:
         return
      else:
         self.message_content += f"\nFor the past three PRs, {category.upper()} has been greater than two standard deviations above the mean for the following tests: \n\n"
         for test, machines in matching.items():
            self.message_content+=f"  * {test}: {(", ").join(machines)}\n"

def main():
   
   message_manager = MessageManager()

   for category in message_manager.categories: 

      message_manager.contents[category] = message_manager.load_json_from_file(os.environ.get(f"{category.upper()}_RESULTS"))
      message_manager.create_message_content(message_manager.contents[category], category)
      
   print(message_manager.message_content)
   
   return message_manager.message_content
   
      

if __name__ == "__main__":

   main()
