# Elasticsearch Transactions Bool And Aggregations Questions

Practice questions for the fake payment transaction data indexed into `app-transactions-*`.

Use this index pattern:

```http
app-transactions-*
```

For these questions, use June 4, 2026 as the exercise day:

```text
2026-06-04T00:00:00Z to before 2026-06-05T00:00:00Z
```

## Fields To Remember

| Field | Use |
| --- | --- |
| `@timestamp` | Filter by day or time window |
| `customer_id` | Count unique users/customers |
| `payment_method` | Filter or group by `card`, `wallet`, `bank_transfer`, `paypal` |
| `status` | Filter or group by transaction state |
| `amount` | Range filters, average, sum, max |
| `risk_score` | Range filters and average risk |
| `latency_ms` | Average latency |
| `currency` | Group amounts by currency |
| `provider` | Group results by payment provider |
| `country` | Group transactions by country |
| `channel` | Filter or group by `web`, `mobile`, `pos`, `api` |
| `card_network` | Group card transactions by card network |
| `fraud_flag` | Boolean filter for suspicious transactions |

## 1. Unique Card Users For The Day

How many unique customers used `card` as the payment method on June 4, 2026?

Think about:

- Use `bool.filter` because both conditions are exact filters.
- Use a `term` filter for `payment_method`.
- Use a `range` filter for `@timestamp`.
- Use a `cardinality` aggregation on `customer_id` to count unique users.

## 2. Status Breakdown For High-Value Card Payments

For card payments with `amount >= 500`, how many transactions are there for each `status`?

Think about:

- Filter first to keep only card payments.
- Add a numeric `range` filter on `amount`.
- Use a `terms` aggregation on `status`.

## 3. Captured Amounts By Currency

For transactions with `status` equal to `captured`, what is the total amount and average amount per `currency`?

Think about:

- Use a `term` filter for `status`.
- Use a `terms` aggregation on `currency`.
- Inside each currency bucket, use `sum` and `avg` on `amount`.

## 4. High-Risk Failed Or Declined Transactions By Provider

For transactions where `status` is `failed` or `declined` and `risk_score >= 0.8`, how many transactions are there by `provider`?

Think about:

- Use `terms` for multiple statuses.
- Use `range` for `risk_score`.
- Use a `terms` aggregation on `provider`.

## 5. Average Latency For Successful Transactions By Payment Method

For successful transactions, what is the average `latency_ms` for each `payment_method`?

Treat `authorized` and `captured` as successful.

Think about:

- Use `terms` to filter `status` to successful values.
- Group with a `terms` aggregation on `payment_method`.
- Add an `avg` aggregation on `latency_ms`.

## 6. Fraud Transactions By Country

How many transactions have `fraud_flag` set to `true` for each `country`?

Think about:

- Use a boolean `term` filter on `fraud_flag`.
- Use a `terms` aggregation on `country`.

## 7. Status Breakdown For Web And Mobile Channels

For transactions from `web` or `mobile`, show the count by `channel`, then by `status`.

Think about:

- Use `terms` to filter `channel`.
- Create a `terms` aggregation on `channel`.
- Add a nested `terms` aggregation on `status`.

## 8. Total Transaction Amount Per Hour

For June 4, 2026, what is the total transaction `amount` per hour?

Think about:

- Filter the data to the exercise day with `@timestamp`.
- Use a `date_histogram` aggregation.
- Inside each time bucket, use a `sum` aggregation on `amount`.

## 9. Card Network Breakdown For Declines And Chargebacks

For card transactions where `status` is `declined` or `chargeback`, how many transactions are there by `card_network`?

Think about:

- Filter `payment_method` to `card`.
- Filter `status` to two values with `terms`.
- Use a `terms` aggregation on `card_network`.

## 10. High-Value Suspicious Payments By Provider

For suspicious high-value payment incidents, group by `provider` and calculate:

- number of transactions
- average `amount`
- maximum `amount`
- average `risk_score`
- status breakdown inside each provider

Use this definition of suspicious:

- `status` is `declined`, `failed`, or `chargeback`
- `amount >= 1000`
- `risk_score >= 0.85`

Think about:

- Use `bool.filter` to combine all incident conditions.
- Use `terms` for the list of statuses.
- Use `range` for `amount` and `risk_score`.
- Group by `provider`.
- Add metric aggregations for `amount` and `risk_score`.
- Add a nested `terms` aggregation on `status`.
