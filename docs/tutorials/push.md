# Push Notifications

Learn how to implement push notifications between OCPI parties.

## Overview

OCPI push notifications allow parties to notify each other about changes to OCPI objects (locations, sessions, CDRs, etc.).

## Implementation

::: ocpi.core.push

## HTTP Push

HTTP push notifications are sent via POST requests to the receiving party's push endpoint.

## WebSocket Push

WebSocket push notifications provide real-time bidirectional communication.

!!! note
    WebSocket push is experimental and may not be supported by all OCPI implementations.
