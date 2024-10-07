import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Read the CSV file into a pandas DataFrame
csv_file = 'api_details.csv'  # Path to your CSV file
df = pd.read_csv(csv_file)

# Normalize column names by stripping spaces and converting to lowercase
df.columns = df.columns.str.strip().str.lower()

# Create the root JMeter test plan element with the correct version and properties
test_plan = ET.Element('jmeterTestPlan', attrib={'version': '1.2', 'properties': '5.0', 'jmeter': '5.1.1 r1855137'})
root_hash_tree = ET.SubElement(test_plan, 'hashTree')

# Create the Test Plan element
test_plan_element = ET.SubElement(root_hash_tree, 'TestPlan', {'guiclass': 'TestPlanGui', 'testclass': 'TestPlan', 'testname': 'Test Plan', 'enabled': 'true'})
ET.SubElement(test_plan_element, 'stringProp', {'name': 'TestPlan.comments'}).text = ''
ET.SubElement(test_plan_element, 'boolProp', {'name': 'TestPlan.functional_mode'}).text = 'false'
ET.SubElement(test_plan_element, 'boolProp', {'name': 'TestPlan.tearDown_on_shutdown'}).text = 'true'
ET.SubElement(test_plan_element, 'boolProp', {'name': 'TestPlan.serialize_threadgroups'}).text = 'false'
user_defined_variables = ET.SubElement(test_plan_element, 'elementProp', {'name': 'TestPlan.user_defined_variables', 'elementType': 'Arguments', 'guiclass': 'ArgumentsPanel', 'testclass': 'Arguments', 'testname': 'User Defined Variables', 'enabled': 'true'})
ET.SubElement(user_defined_variables, 'collectionProp', {'name': 'Arguments.arguments'})
ET.SubElement(test_plan_element, 'stringProp', {'name': 'TestPlan.user_define_classpath'}).text = ''

# Add hashTree after Test Plan
test_plan_hash_tree = ET.SubElement(root_hash_tree, 'hashTree')

# Create the Thread Group
thread_group = ET.SubElement(test_plan_hash_tree, 'ThreadGroup', {'guiclass': 'ThreadGroupGui', 'testclass': 'ThreadGroup', 'testname': 'Thread Group', 'enabled': 'true'})
ET.SubElement(thread_group, 'stringProp', {'name': 'ThreadGroup.on_sample_error'}).text = 'continue'
loop_controller = ET.SubElement(thread_group, 'elementProp', {'name': 'ThreadGroup.main_controller', 'elementType': 'LoopController', 'guiclass': 'LoopControlPanel', 'testclass': 'LoopController', 'testname': 'Loop Controller', 'enabled': 'true'})
ET.SubElement(loop_controller, 'boolProp', {'name': 'LoopController.continue_forever'}).text = 'false'
ET.SubElement(loop_controller, 'stringProp', {'name': 'LoopController.loops'}).text = '1'
ET.SubElement(thread_group, 'stringProp', {'name': 'ThreadGroup.num_threads'}).text = '1'  # Number of threads
ET.SubElement(thread_group, 'stringProp', {'name': 'ThreadGroup.ramp_time'}).text = '1'  # Ramp-up time
ET.SubElement(thread_group, 'boolProp', {'name': 'ThreadGroup.scheduler'}).text = 'false'
ET.SubElement(thread_group, 'stringProp', {'name': 'ThreadGroup.duration'}).text = ''  # No duration
ET.SubElement(thread_group, 'stringProp', {'name': 'ThreadGroup.delay'}).text = ''  # No delay

# Add hashTree after Thread Group
thread_group_hash_tree = ET.SubElement(test_plan_hash_tree, 'hashTree')

# Create the Transaction Controller under Thread Group
transaction_controller = ET.SubElement(thread_group_hash_tree, 'TransactionController', {'guiclass': 'TransactionControllerGui', 'testclass': 'TransactionController', 'testname': 'Transaction Controller', 'enabled': 'true'})
ET.SubElement(transaction_controller, 'boolProp', {'name': 'TransactionController.includeTimers'}).text = 'false'
ET.SubElement(transaction_controller, 'boolProp', {'name': 'TransactionController.parent'}).text = 'false'

# Close the hashTree for TransactionController right after it
transaction_controller_hash_tree = ET.SubElement(thread_group_hash_tree, 'hashTree')

# Helper function to create an HTTP Sampler in JMeter
def create_http_sampler(protocol, domain, port, method, path, body):
    # Remove leading/trailing spaces in protocol and path
    protocol = protocol.strip()
    path = path.strip()

    # Create the HTTP Sampler
    sampler = ET.Element('HTTPSamplerProxy', {'guiclass': 'HttpTestSampleGui', 'testclass': 'HTTPSamplerProxy', 'testname': 'HTTP Request', 'enabled': 'true'})
    
    args_element = ET.SubElement(sampler, 'elementProp', {'name': 'HTTPsampler.Arguments', 'elementType': 'Arguments', 'guiclass': 'HTTPArgumentsPanel', 'testclass': 'Arguments', 'testname': 'User Defined Variables', 'enabled': 'true'})
    ET.SubElement(args_element, 'collectionProp', {'name': 'Arguments.arguments'})
    
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.domain'}).text = domain
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.port'}).text = str(port)
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.protocol'}).text = protocol
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.contentEncoding'}).text = ''
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.path'}).text = path
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.method'}).text = method
    
    # Additional HTTP Sampler properties
    ET.SubElement(sampler, 'boolProp', {'name': 'HTTPSampler.follow_redirects'}).text = 'true'
    ET.SubElement(sampler, 'boolProp', {'name': 'HTTPSampler.auto_redirects'}).text = 'false'
    ET.SubElement(sampler, 'boolProp', {'name': 'HTTPSampler.use_keepalive'}).text = 'true'
    ET.SubElement(sampler, 'boolProp', {'name': 'HTTPSampler.DO_MULTIPART_POST'}).text = 'false'
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.embedded_url_re'}).text = ''
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.connect_timeout'}).text = ''
    ET.SubElement(sampler, 'stringProp', {'name': 'HTTPSampler.response_timeout'}).text = ''
    
    return sampler

# Helper function to create an empty Header Manager
def create_header_manager():
    header_manager = ET.Element('HeaderManager', {'guiclass': 'HeaderPanel', 'testclass': 'HeaderManager', 'testname': 'HTTP Header Manager', 'enabled': 'true'})
    # Create an empty collectionProp
    ET.SubElement(header_manager, 'collectionProp', {'name': 'HeaderManager.headers'})
    return header_manager

# Helper function to create a Response Assertion without extra stringProp
def create_response_assertion():
    response_assertion = ET.Element('ResponseAssertion', {'guiclass': 'AssertionGui', 'testclass': 'ResponseAssertion', 'testname': 'Response Assertion', 'enabled': 'true'})
    ET.SubElement(response_assertion, 'collectionProp', {'name': 'Assertion.test_strings'})  # No stringProp inside
    ET.SubElement(response_assertion, 'stringProp', {'name': 'Assertion.custom_message'}).text = ''
    ET.SubElement(response_assertion, 'stringProp', {'name': 'Assertion.test_field'}).text = 'Assertion.response_data'
    ET.SubElement(response_assertion, 'boolProp', {'name': 'Assertion.assume_success'}).text = 'false'
    ET.SubElement(response_assertion, 'intProp', {'name': 'Assertion.test_type'}).text = '16'  # 16 means "Contains"
    return response_assertion

# Process each row in the CSV and add it to the Transaction Controller
for index, row in df.iterrows():
    protocol = row['protocol']
    domain = row['domain']
    port = row['port']
    method = row['method']
    path = row['path']
    body = row['body']
    
    # Create an HTTP Sampler for each row
    sampler = create_http_sampler(protocol, domain, port, method, path, body)
    
    # Create a Header Manager and Response Assertion
    header_manager = create_header_manager()
    response_assertion = create_response_assertion()
    
    # Add the HTTP Sampler directly under the Transaction Controller's hashTree
    transaction_controller_hash_tree.append(sampler)
    
    # Add Header Manager and Response Assertion under the HTTP sampler
    sampler_hash_tree = ET.SubElement(transaction_controller_hash_tree, 'hashTree')
    sampler_hash_tree.append(header_manager)
    
    # Close hashTree after HeaderManager, then add Response Assertion
    assertion_hash_tree = ET.SubElement(sampler_hash_tree, 'hashTree')
    assertion_hash_tree.append(response_assertion)

# Function to pretty print XML
def pretty_print_xml(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Pretty print the XML tree to a string
xml_str = pretty_print_xml(test_plan)

# Fix the XML declaration to include encoding="UTF-8"
xml_str = xml_str.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')

# Write the formatted XML to a file
with open('jmeter_script.jmx', 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("Formatted JMeter script with corrected structure has been generated successfully.")
