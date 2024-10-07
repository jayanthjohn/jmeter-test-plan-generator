import pandas as pd
import xml.etree.ElementTree as ET

def create_jmeter_script(csv_file, jmeter_script_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Create the root element for JMeter
    jmeter = ET.Element('jmeterTestPlan')
    jmeter.set('version', '1.2')
    jmeter.set('properties', '5.0')
    
    # Add a test plan
    test_plan = ET.SubElement(jmeter, 'TestPlan')
    test_plan.set('guiclass', 'TestPlanGui')
    test_plan.set('testclass', 'TestPlan')
    test_plan.set('testname', 'API Test Plan')
    test_plan.set('enabled', 'true')

    # Add a thread group for each API
    for _, row in df.iterrows():
        # Create a Thread Group
        thread_group = ET.SubElement(jmeter, 'ThreadGroup')
        thread_group.set('guiclass', 'ThreadGroupGui')
        thread_group.set('testclass', 'ThreadGroup')
        thread_group.set('testname', row['api_name'])
        thread_group.set('enabled', 'true')
        
        # Add Transaction Controller
        transaction_controller = ET.SubElement(thread_group, 'TransactionController')
        transaction_controller.set('guiclass', 'TransactionControllerGui')
        transaction_controller.set('testclass', 'TransactionController')
        transaction_controller.set('testname', 'Transaction for ' + row['api_name'])
        transaction_controller.set('enabled', 'true')

        # Create HTTP Sampler
        http_sampler = ET.SubElement(transaction_controller, 'HTTPSamplerProxy')
        http_sampler.set('guiclass', 'HttpTestSampleGui')
        http_sampler.set('testclass', 'HTTPSamplerProxy')
        http_sampler.set('testname', row['api_name'])
        http_sampler.set('enabled', 'true')

        # Set sampler details
        http_sampler.set('protocol', row['protocol'])
        http_sampler.set('domain', row['domain'])
        http_sampler.set('port', str(row['port']))
        http_sampler.set('path', row['path'])
        http_sampler.set('method', row['method'])
        
        # Add HTTP Header Manager
        header_manager = ET.SubElement(http_sampler, 'HeaderManager')
        header_manager.set('guiclass', 'HeaderPanel')
        header_manager.set('testclass', 'HeaderManager')
        header_manager.set('testname', 'HTTP Header Manager')
        header_manager.set('enabled', 'true')

        # Example: Adding a Content-Type header
        content_type = ET.SubElement(header_manager, 'Header')
        content_type.set('name', 'Content-Type')
        content_type.set('value', 'application/json')

        # Add Body Data if the method is not GET
        if row['method'].upper() != 'GET':
            body_data = ET.SubElement(http_sampler, 'BodyData')
            body_data.text = row['body']

        # Add Response Assertion
        response_assertion = ET.SubElement(http_sampler, 'ResponseAssertion')
        response_assertion.set('guiclass', 'ResponseAssertionGui')
        response_assertion.set('testclass', 'ResponseAssertion')
        response_assertion.set('testname', 'Response Assertion for ' + row['api_name'])
        response_assertion.set('enabled', 'true')

        # Add assertions to check for a successful response code
        response_field = ET.SubElement(response_assertion, 'collectionType')
        response_field.text = '0'  # Check response code

        # Add a response code to assert (e.g., 200)
        response_code = ET.SubElement(response_assertion, 'testField')
        response_code.set('test_field', 'Response Code')
        response_code.text = '200'  # Expecting HTTP 200 OK

    # Create a tree from the root and write to an XML file
    tree = ET.ElementTree(jmeter)
    tree.write(jmeter_script_file, encoding='utf-8', xml_declaration=True)

# Example usage
csv_file = 'api_details.csv'  # Path to your CSV file
jmeter_script_file = 'generated_test_plan.jmx'  # Output JMeter script file
create_jmeter_script(csv_file, jmeter_script_file)
