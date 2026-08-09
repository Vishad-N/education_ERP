ARG FRAPPE_TAG=v16.19.0
ARG FRAPPE_SHA=ba18090b141740e75d52aa97bfc525ff2f831f6c
ARG ERPNEXT_TAG=v16.22.0
ARG ERPNEXT_SHA=054b20a2ae1bdea44694cca72d17412945171cab
ARG EDUCATION_SHA=1c29e646bf943c2a5f696cb81cb48c8a072cbebc
ARG CRM_TAG=v1.72.0
ARG CRM_SHA=bf1b7f07ac01b6ac435f25db7ccef6b52807720e
ARG PAYMENTS_SHA=cca07d9f9392e2ea0e521c5975151db9e4b6c321
ARG BENCH_IMAGE=frappe/bench:v5.31.0

FROM ${BENCH_IMAGE}

ARG FRAPPE_TAG
ARG FRAPPE_SHA
ARG ERPNEXT_TAG
ARG ERPNEXT_SHA
ARG EDUCATION_SHA
ARG CRM_TAG
ARG CRM_SHA
ARG PAYMENTS_SHA

USER frappe
WORKDIR /home/frappe

COPY --chown=frappe:frappe apps.json /tmp/apps.json

RUN bench init frappe-bench --frappe-branch ${FRAPPE_TAG} --skip-redis-config-generation \
    && cd frappe-bench/apps/frappe \
    && test "$(git rev-parse HEAD)" = "${FRAPPE_SHA}"

WORKDIR /home/frappe/frappe-bench

RUN bench get-app erpnext https://github.com/frappe/erpnext \
    && cd apps/erpnext \
    && git fetch --depth 1 origin ${ERPNEXT_SHA} \
    && git checkout ${ERPNEXT_SHA} \
    && cd ../.. \
    && bench get-app education https://github.com/frappe/education \
    && cd apps/education \
    && git fetch --depth 1 origin ${EDUCATION_SHA} \
    && git checkout ${EDUCATION_SHA} \
    && cd ../.. \
    && bench get-app --branch ${CRM_TAG} crm https://github.com/frappe/crm \
    && cd apps/crm \
    && test "$(git rev-parse HEAD)" = "${CRM_SHA}" \
    && cd ../.. \
    && bench get-app payments https://github.com/frappe/payments \
    && cd apps/payments \
    && git fetch --depth 1 origin ${PAYMENTS_SHA} \
    && git checkout ${PAYMENTS_SHA}

COPY --chown=frappe:frappe docker/config/common_site_config.json sites/common_site_config.json

ENV PATH="/home/frappe/frappe-bench/env/bin:${PATH}"
