def test_home_route():
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    
    assert response.status_code == 200