const axios = require('axios');
jest.mock('axios');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const { tryURLs } = require('../src/api');

// Mocking XMLHttpRequest
function mockXMLHttpRequest() {
  const mock = {
    open: jest.fn(),
    send: jest.fn().mockImplementation(function () {
      if (this.onreadystatechange) {
        this.onreadystatechange();
      }
    }),
    setRequestHeader: jest.fn(),
    onreadystatechange: null,
    readyState: 4,
    status: 200,
    responseText: JSON.stringify({ data: 'mocked data' }),
  };
  return mock;
}

// Setting up the global environment for the tests
const htmlFilePath = path.join(__dirname, '..', 'src', 'index.html');
const htmlContent = fs.readFileSync(htmlFilePath, 'utf8');
const dom = new JSDOM(htmlContent, { runScripts: "dangerously", resources: "usable" });

// Define the global document and window based on JSDOM
global.document = dom.window.document;
global.window = dom.window;
// Assign the mock XMLHttpRequest to the global scope
global.XMLHttpRequest = jest.fn(() => mockXMLHttpRequest());

describe('tryURLs function', () => {
  let mockXHR;

  beforeEach(() => {
    // Resetting mocks before each test
    mockXHR = mockXMLHttpRequest();
    global.XMLHttpRequest.mockClear();
    global.XMLHttpRequest.mockImplementation(() => mockXHR);
    axios.get.mockClear(); // Clears any previous mock
  });

  test('success case', done => {
    axios.get.mockResolvedValue({ data: 'mocked data' }); // Mock axios for success scenario

    const successCallback = jest.fn();
    const errorCallback = jest.fn();

    // Define the onreadystatechange handler to simulate the success handling
    mockXHR.onreadystatechange = () => {
      if (mockXHR.readyState === 4 && mockXHR.status === 200) {
        successCallback(JSON.parse(mockXHR.responseText));
      }
    };

    // Call the function with the test data
    tryURLs(['http://localhost:81/?'], 'test=query', successCallback, errorCallback);

    // Trigger the readyState change
    mockXHR.onreadystatechange();

    // Process the next event loop
    setImmediate(() => {
      // Assertions to verify the behavior
      expect(successCallback).toHaveBeenCalledWith({ data: 'mocked data' });
      expect(errorCallback).not.toHaveBeenCalled();
      expect(mockXHR.open).toHaveBeenCalledWith("GET", 'http://localhost:81/?test=query', true);
      expect(mockXHR.send).toHaveBeenCalled();
      done();
    });
  });

  test('error case', done => {
    axios.get.mockRejectedValue(new Error('mock error')); // Mock axios for error scenario

    const successCallback = jest.fn();
    const errorCallback = jest.fn();

    // Define the onreadystatechange handler to simulate the error handling
    mockXHR.onreadystatechange = () => {
      if (mockXHR.readyState === 4 && mockXHR.status !== 200) {
        errorCallback(JSON.parse(mockXHR.responseText).message);
      }
    };

    // Call the function with the test data
    tryURLs(['http://mockurl.com/?'], 'test=query', successCallback, errorCallback);

    // Adjust the mock object to represent an error state
    mockXHR.status = 400;
    mockXHR.responseText = JSON.stringify({ message: 'Error occurred' });

    // Trigger the readyState change
    mockXHR.onreadystatechange();

    // Process the next event loop
    setImmediate(() => {
      // Assertions to verify the behavior
      expect(errorCallback).toHaveBeenCalledWith('Error occurred');
      expect(successCallback).not.toHaveBeenCalled();
      expect(mockXHR.open).toHaveBeenCalledWith("GET", 'http://mockurl.com/?test=query', true);
      expect(mockXHR.send).toHaveBeenCalled();
      done();
    });
  });
});
