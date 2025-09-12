#!/usr/bin/env bash
curl -X POST "http://localhost:8999/get-online-features" -d '{
    "features": [
      "customer_credit_risk_feature_view:purpose_business"
    ],
    "entities": {
      "entity_id": [0,1,2]
    }
}'