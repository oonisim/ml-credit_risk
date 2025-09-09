#!/usr/bin/env bash
git push https://oonisim:$(cat ${HOME}/.github/tokyo/token | tr -d '\n')@github.com/oonisim/ml-credit_risk.git
