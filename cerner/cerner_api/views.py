# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import urllib
from django.http import HttpResponse
from urllib2 import Request, urlopen
from json import load, dump, dumps, loads

from django.http import HttpResponse
from django.template import Context, loader
import requests
from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from xml.etree import ElementTree

def authDetails(request):
	accessTokenUrl = 'https://authorization.sandboxcerner.com/tenants/0b8a0111-e8e6-4c26-a91c-5069cbc6b1ca/protocols/oauth2/profiles/smart-v1/token'
	ccdaUrl = 'https://fhir-ehr.sandboxcerner.com/dstu2/0b8a0111-e8e6-4c26-a91c-5069cbc6b1ca/Binary/$autogen-ccd-if?patient='
	patientUrl = 'https://fhir-ehr.sandboxcerner.com/dstu2/0b8a0111-e8e6-4c26-a91c-5069cbc6b1ca/Patient/'
	code = request.GET.get('code')
	state = request.GET.get('state')
	data = {
		'code': code,
		'grant_type': 'authorization_code',
		'client_id': 'ee5690bb-ac02-4be0-a272-1f978906c0ef',
		'redirect_uri': 'http://localhost:8000/'
	}

	with requests.Session() as session:
		data = session.post(accessTokenUrl, data=data, verify=True)

	accessTokenData = loads(data.content)
	accessToken = accessTokenData["access_token"]
	patient = accessTokenData["patient"]

	# Access Token
	print(accessTokenData["access_token"], "access token")
	
	# User Details
	print(accessTokenData["username"], "username")
	print(accessTokenData["user"], "user")

	patientUrl = patientUrl + patient
	patientDetailsRequest = Request(
		patientUrl,
		None,
		{
			'Accept': 'application/json+fhir',
			'Authorization': 'Bearer ' + accessToken
		}
	)
	patientDetails = load(urlopen(patientDetailsRequest))

	# Patient Details
	print(patientDetails, "patient details")

	ccdaUrl = ccdaUrl + patient
	ccdaRequest = Request(
		ccdaUrl,
		None,
		{
			'Accept': 'application/xml',
			'Authorization': 'Bearer ' + accessToken
		}
	)
	ccdaDocument = urlopen(ccdaRequest)

	# CCDA Document Data
	return HttpResponse(ccdaDocument)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


