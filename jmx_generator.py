import csv
from jinja2 import Template

# Sample JMeter XML template using Jinja2
jmeter_template = """
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="Test Plan">
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
    </TestPlan>
    <hashTree>
      {% for api in apis %}
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="{{ api['api_name'] }} Thread Group">
        <intProp name="ThreadGroup.num_threads">1</intProp>
        <intProp name="ThreadGroup.ramp_time">1</intProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller">
          <stringProp name="LoopController.loops">1</stringProp>
          <boolProp name="LoopController.continue_forever">false</boolProp>
        </elementProp>
      </ThreadGroup>
      <hashTree>
        <TransactionController guiclass="TransactionControllerGui" testclass="TransactionController" testname="{{ api['api_name'] }} Transaction Controller"/>
        <hashTree>
          <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{{ api['api_name'] }} HTTP Request">
            <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
            <stringProp name="HTTPSampler.method">{{ api['method'] }}</stringProp>
            <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
            <stringProp name="HTTPSampler.protocol">{{ api['protocol'] }}</stringProp>
            <stringProp name="HTTPSampler.domain">{{ api['domain'] }}</stringProp>
            <stringProp name="HTTPSampler.port">{{ api['port'] }}</stringProp>
            <stringProp name="HTTPSampler.path">{{ api['path'] }}</stringProp>
            {% if api['method'] != 'GET' %}
            <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
            <stringProp name="HTTPSampler.arguments">{{ api['body'] }}</stringProp>
            {% else %}
            <boolProp name="HTTPSampler.postBodyRaw">false</boolProp>
            {% endif %}
          </HTTPSamplerProxy>
          <hashTree>
            <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP Header Manager">
              <collectionProp name="HeaderManager.headers"/>
            </HeaderManager>
            <hashTree/>
            <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Response Assertion">
              <collectionProp name="Assertion.test_strings"/>
              <stringProp name="Assertion.custom_message"></stringProp>
              <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
              <boolProp name="Assertion.assume_success">false</boolProp>
              <intProp name="Assertion.test_type">16</intProp>
            </ResponseAssertion>
            <hashTree/>
          </hashTree>
        </hashTree>
      </hashTree>
      {% endfor %}
    </hashTree>
  </hashTree>
</jmeterTestPlan>
"""

# Load CSV data
def load_api_data(csv_file):
    apis = []
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            apis.append(row)
    return apis

# Render the JMeter template with data from the CSV
def generate_jmeter_script(csv_file, output_file):
    apis = load_api_data(csv_file)
    
    # Initialize the Jinja2 template
    template = Template(jmeter_template)
    
    # Render the template with the data
    jmeter_script = template.render(apis=apis)
    
    # Write the JMeter script to a file
    with open(output_file, 'w') as file:
        file.write(jmeter_script)

# Usage
csv_file = 'api_details.csv'  # Input CSV file
output_file = 'test_plan.jmx'  # Output JMX file
generate_jmeter_script(csv_file, output_file)
