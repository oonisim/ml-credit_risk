#!/usr/bin/env bash
feast serve
curl -X POST "http://localhost:6566/get-online-features" -d '{
    "features": [
      "customer_credit_risk_feature_view:purpose_business"
    ],
    "entities": {
      "entity_id": [1,2]
    }
}'
