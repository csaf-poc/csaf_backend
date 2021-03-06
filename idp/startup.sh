#!/bin/bash
cat /tmp/csaf-realm.tpl.json | sed -E 's/\"secret\":\s*\"[^\"]*\"/\"secret\": \"'"$OIDC_CLIENT_SECRET"'\"/g' > /tmp/csaf-realm.json