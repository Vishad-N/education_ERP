ARG FRAPPE_VERSION=v16.19.0
ARG ERPNEXT_VERSION=v16.22.0
ARG EDUCATION_REF=version-16
ARG CRM_VERSION=v1.72.0

FROM frappe/bench:latest

ARG FRAPPE_VERSION
ARG ERPNEXT_VERSION
ARG EDUCATION_REF
ARG CRM_VERSION

USER frappe
WORKDIR /home/frappe

RUN bench init frappe-bench --frappe-branch ${FRAPPE_VERSION} --skip-redis-config-generation

WORKDIR /home/frappe/frappe-bench

RUN bench get-app --branch ${ERPNEXT_VERSION} erpnext https://github.com/frappe/erpnext \
    && bench get-app --branch ${EDUCATION_REF} education https://github.com/frappe/education \
    && bench get-app --branch ${CRM_VERSION} crm https://github.com/frappe/crm \
    && bench get-app --branch version-16 payments https://github.com/frappe/payments

COPY --chown=frappe:frappe docker/config/common_site_config.json sites/common_site_config.json

ENV PATH="/home/frappe/frappe-bench/env/bin:${PATH}"
