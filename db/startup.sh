#!/bin/bash
set -e

echo "[:] Add database user"
if [ -n "${MONGO_INITDB_DATABASE:-}" ] \
	&& [ -n "${MONGO_INITDB_ROOT_USERNAME:-}" ] \
	&& [ -n "${MONGO_INITDB_ROOT_PASSWORD:-}" ] \
	&& [ -n "${MONGODB_USERNAME:-}" ] \
	&& [ -n "${MONGODB_PASSWORD:-}" ]; then
	mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD << EOF
	db=db.getSiblingDB('csaf_advisory_db');
	db.createUser(
	    {
	        user: '$MONGODB_USERNAME',
	        pwd: '$MONGODB_PASSWORD',
	        roles: [
	            {
	                role: "readWrite",
	                db: "csaf_advisory_db"
	            }
	        ]
	    }
	);
EOF
else
	echo "[!] Missing environment variables"
	exit 403
fi
echo "[+] Done"