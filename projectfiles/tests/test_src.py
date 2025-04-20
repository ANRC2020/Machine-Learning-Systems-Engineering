from fastapi.testclient import TestClient
from src.main import app
import random
import string
import datetime

def get_random_name() -> str:

    length = random.randint(1, 10)

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

client = TestClient(app)

def test_health():

    with TestClient(app) as client:
            response = client.get("/lab/health") 

    # There enpoint should return 200 status code
    assert response.status_code == 200

    # The json being sent back should be {"time": str(datetime.now().isoformat())}
    response_time = datetime.datetime.fromisoformat(response.json()['time'])
    current_time = datetime.datetime.now()

    if abs(response_time - current_time) <= datetime.timedelta(seconds=2):
        assert response.status_code == 200
    else:
        assert response.status_code == 500

def test_hello_improper_request():

    with TestClient(app) as client:
            response = client.get(f"/lab/hello")
    
    # The api expects a an additional argument to be passed so we it should return 422 status code
    assert response.status_code == 422

def test_hello_proper_request():

    with TestClient(app) as client:

        for i in range(10):
            new_name = get_random_name()

            response = client.get(f"/lab/hello?name={new_name}")
    
            # The api should return a 200 status code
            assert response.status_code == 200

            assert response.json() == {"message": f"Hello {new_name}"}

def test_root():
    response = client.get("/")
    
    # There is no enpoint set for ("/") so we expect a 404
    assert response.status_code == 404

def test_doc():
    
    with TestClient(app) as client:
        response = client.get("/lab/docs")

    # The api should return a 200 status code
    assert response.status_code == 200

def test_openapi():

    with TestClient(app) as client:
        response = client.get("/lab/openapi.json")

    # The api should return a 200 status code
    assert response.status_code == 200
    
def test_predict_wrong_type():
    
    data = {"MedInc": 'Hello', # Passing in the wrong item
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": 0}

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_predict_missing_value():
    
    data = {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            # "AveOccup": 2.7, # Omit this value
            "Latitude": 45,
            "Longitude": 0}

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_predict_extra_value():
    
    data = {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": 0,
            "Extra":2}

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_predict_extra_and_missing_value():
    
    data = {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            # "Population": 322.0, # Missing value
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": 0,
            "Extra":2}

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_predict_incorrect_latitude():
    
    data = {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 91,
            "Longitude": 90}

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_predict_incorrect_longitude():
    
    data = {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": -190}

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_predict_correct():
    
    data = {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": 90}

    # Send a POST request
    # response = client.post("/lab/predict", json=data)

    with TestClient(app) as client:
        response = client.post("/lab/predict", json=data)

    # Check the response status code
    assert response.status_code == 200
    
    # The prediction being returned should be a float
    assert type(response.json()['prediction']) == float

def test_bulk_predict_incorrect_longitude():
    
    data = [{"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": -190},
            {"MedInc": 8.32,
            "HouseAge": 41.0,
            "AveRooms": 6.5,
            "AveBedrms": 1.1,
            "Population": 322.0,
            "AveOccup": 2.7,
            "Latitude": 45,
            "Longitude": 90}]

    # Send a POST request
    response = client.post("/lab/bulk-predict", json=data)

    # Check the response status code
    assert response.status_code == 422

def test_bulk_predict_correct():
    
    data = {
            "houses":
                [{"MedInc": 8.32,
                "HouseAge": 41.0,
                "AveRooms": 6.5,
                "AveBedrms": 1.1,
                "Population": 322.0,
                "AveOccup": 2.7,
                "Latitude": 45,
                "Longitude": 0},
                {"MedInc": 5.50,
                "HouseAge": 30.0,
                "AveRooms": 7.2,
                "AveBedrms": 1.0,
                "Population": 210.0,
                "AveOccup": 3.0,
                "Latitude": 36,
                "Longitude": -122},
                {"MedInc": 2.75,
                "HouseAge": 50.0,
                "AveRooms": 4.5,
                "AveBedrms": 1.2,
                "Population": 150.0,
                "AveOccup": 2.5,
                "Latitude": 40,
                "Longitude": -90}]
            }

    # Send a POST request
    with TestClient(app) as client:
        response = client.post("/lab/bulk-predict", json=data)

    # Check the response status code
    assert response.status_code == 200
    
    # The prediction being returned should be a float
    assert type(response.json()['predictions']) == list

    for entry in response.json()['predictions']:
        assert type(entry) == float
