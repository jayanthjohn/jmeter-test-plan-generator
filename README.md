This Python script (jmx_generator.py) generates a JMeter .jmx test plan file from a CSV file containing API details. Each API request is represented as a separate Thread Group in the test plan, with a Transaction Controller and HTTP Sampler. The generated JMeter test plan can then be used for performance testing in JMeter.
**Features**
    •	Generates a JMeter test plan with one Thread Group per API request.
    •	Supports both GET and POST (or other) HTTP methods.
    •	Automatically creates an HTTP Sampler with the specified headers, protocol, domain, port, method, and path.
    •	Adds a Response Assertion and HTTP Header Manager for each API.
    •	The POST requests automatically include the request body from the CSV.
**Prerequisites**
    •	Python 3.x
    •	Jinja2 template engine
    •	A CSV file containing the API details in the specified format.
**Installation**
1.	Clone the repository:

git clone https://github.com/yourusername/jmeter-csv-script-generator.git
cd jmeter-csv-script-generator
2.	Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
**CSV File Format**
The CSV file should contain the following columns:
    •	api_name: The name of the API (used to name the thread group and HTTP sampler).
    •	protocol: The protocol to be used (e.g., http or https).
    •	domain: The domain of the API (e.g., www.example.com).
    •	port: The port number (e.g., 80 for HTTP or 443 for HTTPS).
    •	method: The HTTP method (e.g., GET, POST).
    •	path: The endpoint path (e.g., /users).
    •	body: The body of the request (only for methods like POST, PUT, etc.).
**Example CSV**
csv
api_name,protocol,domain,port,method,path,body
UserAPI,https,www.example.com,443,GET,/users,
ProductAPI,https,api.example.com,443,POST,/users,"{\"name\":\"Product\",\"price\":100}"
OrderAPI,http,orders.example.com,80,GET,/orders,
SampleProduct,http,orders.example.com,667,POST,/new/old,"{\"name\":\"Product\",\"price\":100}"

**Usage**
1.	Place your CSV file in the project directory. For example, api_details.csv.
2.	Run the script to generate the JMeter .jmx file:

python jmx_generator.py
3.	The generated JMeter test plan will be saved as test_plan.jmx.

**Script Overview**
The script does the following:
    •	Reads the API details from the CSV file.
    •	For each API, it creates a Thread Group, Transaction Controller, HTTP Sampler, HTTP Header Manager, and Response Assertion.
    •	If the HTTP method is POST or any other method with a body, it includes the body from the CSV in the HTTP Sampler.

**Example**
If your CSV file is named api_details.csv, you can generate a JMeter script like this:
python jmx_generator.py
The output will be saved as **test_plan.jmx**, ready to be opened in JMeter.
**Customization**
You can modify the script or the Jinja2 template to suit your specific requirements, such as:
    •	Adding additional request headers.
    •	Handling other HTTP methods.
    •	Customizing thread group properties.

