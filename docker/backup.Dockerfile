FROM mariadb:11.8

COPY scripts/operations/backup-mariadb.sh /usr/local/bin/backup-mariadb.sh
COPY scripts/operations/restore-mariadb.sh /usr/local/bin/restore-mariadb.sh
RUN chmod 0755 /usr/local/bin/backup-mariadb.sh /usr/local/bin/restore-mariadb.sh

ENTRYPOINT ["/usr/local/bin/backup-mariadb.sh"]
