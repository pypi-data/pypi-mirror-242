# XFHIR Python SDK


```python

import xfhir
xfhir.init(client_id='xxx', client_secret='xxxx')
xfhir.create({})
xfhir.get(id='', resource_type='Patient')
xfhir.filter(resource_type='Patient', q='')
xfhir.search(q='')
```







Connect to the XFHIR Service
```python
from xfhir import XFHIR
x = XFHIR(client_id='xxx', client_secret='xxxx')

```

Create a Policy for a FHIR Resource
```python
patient_redact_policy = x.policy.create(effect='Redact', actions=[
   'account-id:client-id:method:resource:path',
   'account-id:*:Read:Patient:$',
])
```

Create the FHIR Resource on XFHIR along with its resource policies
```python
x.create({
   'fhir_resource': {},
   'policies': [
      patient_redact_policy
   ]
})

```

Full example
```python
from xfhir import XFHIR
x = XFHIR(client_id='xxx', client_secret='xxxx')

patient_redact_policy = x.policy.create(effect='Redact', actions=[
   'account-id:client-id:method:resource:path',
   'account-id:*:Read:Patient:$',
])

x.create({
   'fhir_resource': {},
   'policies': [
      patient_redact_policy
   ]
})

patient = x.get('Patient', 'identifier')
```

The output of the patient object should be

```json

{
   "id": "*** REDACTED **",
   "name": "*** REDACTED **"
}
```


To redact only a few fields in the patient object you can create a policy that only redacts your custom fields
```python

patient_redact_policy = x.policy.create(effect='Redact', actions=[
   'account-id:*:Read:Patient:$.id',
   'account-id:*:Read:Patient:$.name',
   'account-id:*:Read:Patient:$.contact'   
])

```