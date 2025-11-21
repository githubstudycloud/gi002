package com.enterprise.common.core.util;

import java.security.SecureRandom;
import java.time.Instant;
import java.util.UUID;

/**
 * ID Generator Utility
 * Provides various ID generation strategies
 */
public class IdGenerator {

    private static final SecureRandom RANDOM = new SecureRandom();

    // Snowflake-like ID generator components
    private static final long EPOCH = 1700000000000L; // 2023-11-14 22:13:20 UTC
    private static final long WORKER_ID_BITS = 5L;
    private static final long DATACENTER_ID_BITS = 5L;
    private static final long SEQUENCE_BITS = 12L;

    private static final long MAX_WORKER_ID = ~(-1L << WORKER_ID_BITS);
    private static final long MAX_DATACENTER_ID = ~(-1L << DATACENTER_ID_BITS);

    private static final long WORKER_ID_SHIFT = SEQUENCE_BITS;
    private static final long DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS;
    private static final long TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS;
    private static final long SEQUENCE_MASK = ~(-1L << SEQUENCE_BITS);

    private static long workerId = 1L;
    private static long datacenterId = 1L;
    private static long sequence = 0L;
    private static long lastTimestamp = -1L;

    private IdGenerator() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Generate UUID (without hyphens)
     */
    public static String uuid() {
        return UUID.randomUUID().toString().replace("-", "");
    }

    /**
     * Generate UUID with hyphens
     */
    public static String uuidWithHyphens() {
        return UUID.randomUUID().toString();
    }

    /**
     * Generate Snowflake-like distributed ID
     */
    public static synchronized long snowflakeId() {
        long timestamp = currentTimeMillis();

        if (timestamp < lastTimestamp) {
            throw new RuntimeException("Clock moved backwards. Refusing to generate id");
        }

        if (timestamp == lastTimestamp) {
            sequence = (sequence + 1) & SEQUENCE_MASK;
            if (sequence == 0) {
                timestamp = waitNextMillis(lastTimestamp);
            }
        } else {
            sequence = 0L;
        }

        lastTimestamp = timestamp;

        return ((timestamp - EPOCH) << TIMESTAMP_SHIFT)
                | (datacenterId << DATACENTER_ID_SHIFT)
                | (workerId << WORKER_ID_SHIFT)
                | sequence;
    }

    /**
     * Generate nano ID (URL-friendly unique string)
     */
    public static String nanoId() {
        return nanoId(21);
    }

    /**
     * Generate nano ID with custom length
     */
    public static String nanoId(int length) {
        String alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            sb.append(alphabet.charAt(RANDOM.nextInt(alphabet.length())));
        }
        return sb.toString();
    }

    /**
     * Generate timestamp-based ID (sortable)
     */
    public static String timestampId() {
        return Instant.now().toEpochMilli() + "-" + nanoId(8);
    }

    /**
     * Set worker ID for Snowflake ID generation
     */
    public static void setWorkerId(long id) {
        if (id > MAX_WORKER_ID || id < 0) {
            throw new IllegalArgumentException(
                    String.format("Worker ID must be between 0 and %d", MAX_WORKER_ID));
        }
        workerId = id;
    }

    /**
     * Set datacenter ID for Snowflake ID generation
     */
    public static void setDatacenterId(long id) {
        if (id > MAX_DATACENTER_ID || id < 0) {
            throw new IllegalArgumentException(
                    String.format("Datacenter ID must be between 0 and %d", MAX_DATACENTER_ID));
        }
        datacenterId = id;
    }

    private static long currentTimeMillis() {
        return System.currentTimeMillis();
    }

    private static long waitNextMillis(long lastTimestamp) {
        long timestamp = currentTimeMillis();
        while (timestamp <= lastTimestamp) {
            timestamp = currentTimeMillis();
        }
        return timestamp;
    }
}
