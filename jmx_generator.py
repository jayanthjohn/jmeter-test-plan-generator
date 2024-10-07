from csv import reader
from jmeter import JMeter, ThreadGroup, TransactionController, HttpSampler, HttpHeaderManager, ResponseAssertion

def generate_jmeter_script(csv_file, output_file):
  # Create JMeter instance
  jmeter = JMeter(output_file)

  # Read CSV data
  with open(csv_file, 'r') as csvfile:
    csv_reader = reader(csvfile)
    headers = next(csv_reader)

    # Skip header row
    for row in csv_reader:
      api_name, protocol, domain, port, method, path, body = row

      # Create Thread Group
      thread_group = ThreadGroup(api_name)
      jmeter.add(thread_group)

      # Create Transaction Controller
      transaction_controller = TransactionController(api_name)
      thread_group.add(transaction_controller)

      # Create HTTP Sampler
      http_sampler = HttpSampler(api_name, protocol, domain, port, path)
      # Set method based on data
      http_sampler.set_method(method)
      # Add body for non-GET requests
      if method.upper() != "GET":
        http_sampler.set_body(body)
      transaction_controller.add(http_sampler)

      # Add HTTP Header Manager (optional, you can customize this)
      headers_manager = HttpHeaderManager()
      headers_manager.add_header("Content-Type", "application/json")  # Example header
      transaction_controller.add(headers_manager)

      # Add Response Assertion (optional, you can customize this)
      response_assertion = ResponseAssertion()
      response_assertion.set_response_field_to_test("body")
      response_assertion.add_equals_assertion("Success", "true")  # Example assertion
      transaction_controller.add(response_assertion)

  # Save JMeter script
  jmeter.save()

# Example usage
csv_file = "api_details.csv"
output_file = "generated_test_plan.jmx"
generate_jmeter_script(csv_file, output_file)

print(f"JMeter script generated: {output_file}")
