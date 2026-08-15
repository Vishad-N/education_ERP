ARG FRAPPE_TAG=v16.19.0
ARG FRAPPE_SHA=ba18090b141740e75d52aa97bfc525ff2f831f6c
ARG ERPNEXT_TAG=v16.22.0
ARG ERPNEXT_SHA=054b20a2ae1bdea44694cca72d17412945171cab
ARG EDUCATION_SHA=1c29e646bf943c2a5f696cb81cb48c8a072cbebc
ARG CRM_TAG=v1.72.0
ARG CRM_SHA=bf1b7f07ac01b6ac435f25db7ccef6b52807720e
ARG PAYMENTS_SHA=cca07d9f9392e2ea0e521c5975151db9e4b6c321
ARG BENCH_IMAGE=frappe/bench:v5.31.0@sha256:e44c7454500296940d26ef45eefff8fc295b9d9aacaac4e5714e8be01c326ee8

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

RUN git init apps/erpnext \
    && git -C apps/erpnext remote add origin https://github.com/frappe/erpnext.git \
    && git -C apps/erpnext fetch --depth 1 origin "${ERPNEXT_SHA}" \
    && git -C apps/erpnext checkout --detach FETCH_HEAD \
    && test "$(git -C apps/erpnext rev-parse HEAD)" = "${ERPNEXT_SHA}"

RUN git init apps/education \
    && git -C apps/education remote add origin https://github.com/frappe/education.git \
    && git -C apps/education fetch --depth 1 origin "${EDUCATION_SHA}" \
    && git -C apps/education checkout --detach FETCH_HEAD \
    && test "$(git -C apps/education rev-parse HEAD)" = "${EDUCATION_SHA}"

RUN git init apps/crm \
    && git -C apps/crm remote add origin https://github.com/frappe/crm.git \
    && git -C apps/crm fetch --depth 1 origin "${CRM_SHA}" \
    && git -C apps/crm checkout --detach FETCH_HEAD \
    && test "$(git -C apps/crm rev-parse HEAD)" = "${CRM_SHA}"

RUN git init apps/payments \
    && git -C apps/payments remote add origin https://github.com/frappe/payments.git \
    && git -C apps/payments fetch --depth 1 origin "${PAYMENTS_SHA}" \
    && git -C apps/payments checkout --detach FETCH_HEAD \
    && test "$(git -C apps/payments rev-parse HEAD)" = "${PAYMENTS_SHA}"

RUN bench setup requirements erpnext education crm payments

# Build each pinned app in its own cacheable layer. This keeps retries bounded
# when a frontend build is interrupted by the container engine.
RUN bench build --app erpnext
RUN bench build --app education
RUN NODE_OPTIONS=--max-old-space-size=1536 bench build --app crm
RUN bench build --app payments

RUN rm -rf apps/erpnext/.git apps/education/.git apps/crm/.git apps/payments/.git

# Keep the project-controlled app in a separate layer so routine changes do not
# invalidate the expensive pinned upstream dependency and asset build.
COPY --chown=frappe:frappe apps/university_erp apps/university_erp

RUN env/bin/pip install --editable apps/university_erp \
    && (grep -qxF "university_erp" sites/apps.txt || printf "\nuniversity_erp\n" >> sites/apps.txt) \
    && bench build --app university_erp

COPY --chown=frappe:frappe docker/config/common_site_config.json sites/common_site_config.json
COPY --chown=frappe:frappe scripts/deploy/start-service.sh /home/frappe/frappe-bench/start-service.sh

RUN chmod 0755 /home/frappe/frappe-bench/start-service.sh

ENV PATH="/home/frappe/frappe-bench/env/bin:${PATH}"
