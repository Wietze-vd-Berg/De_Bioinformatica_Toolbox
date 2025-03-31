import sys
import os

import pytest
from Website.app import app


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_index(client):
    resp = client.get('/index.html')
    assert resp.status_code == 200


def test_salmon_invoer(client):
    resp = client.get('/salmon_invoer.html')
    assert resp.status_code == 200


def test_contact(client):
    response = client.get('/contact')
    assert response.status_code == 200


def test_valid_voorbeeld(client):
    response = client.get('/Website/voorbeeld_data/quant.sf')
    assert response.status_code == 200


def test_post(client):
    data = {"name" : "fasta-file", "filename":"Pis_refseq_protein.fasta"}
    response = client.post('/Website/salmon_invoer', data=data)
    assert response.status_code == 200
    print(response.data)