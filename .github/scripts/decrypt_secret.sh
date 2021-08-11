mkdir $HOME/secrets
echo $HOME
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output $HOME/secrets/secrets.json secrets.json.gpg
