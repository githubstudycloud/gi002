package com.enterprise.framework.security.jwt;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.jspecify.annotations.Nullable;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Date;
import java.util.stream.Collectors;

/**
 * JWT Token Provider
 * Using jjwt 0.12.x (latest version compatible with Spring Boot 4.x)
 */
@Slf4j
@Component
public class JwtTokenProvider {

    @Value("${security.jwt.secret:MySecretKeyForJWTTokenGenerationMustBeLongEnough}")
    private String jwtSecret;

    @Value("${security.jwt.expiration:86400000}") // 24 hours in milliseconds
    private Long jwtExpiration;

    @Value("${security.jwt.refresh-expiration:604800000}") // 7 days in milliseconds
    private Long refreshExpiration;

    /**
     * Generate JWT token from authentication
     */
    public String generateToken(Authentication authentication) {
        return generateToken(authentication.getName(), authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.toList()));
    }

    /**
     * Generate JWT token from username and roles
     */
    public String generateToken(String username, @Nullable Object roles) {
        Instant now = Instant.now();
        Instant expiryDate = now.plusMillis(jwtExpiration);

        var builder = Jwts.builder()
                .subject(username)
                .issuedAt(Date.from(now))
                .expiration(Date.from(expiryDate))
                .signWith(getSigningKey());

        if (roles != null) {
            builder.claim("roles", roles);
        }

        return builder.compact();
    }

    /**
     * Generate refresh token
     */
    public String generateRefreshToken(String username) {
        Instant now = Instant.now();
        Instant expiryDate = now.plusMillis(refreshExpiration);

        return Jwts.builder()
                .subject(username)
                .issuedAt(Date.from(now))
                .expiration(Date.from(expiryDate))
                .claim("type", "refresh")
                .signWith(getSigningKey())
                .compact();
    }

    /**
     * Get username from JWT token
     */
    @Nullable
    public String getUsernameFromToken(String token) {
        try {
            Claims claims = getClaims(token);
            return claims.getSubject();
        } catch (Exception e) {
            log.error("Failed to get username from token", e);
            return null;
        }
    }

    /**
     * Validate JWT token
     */
    public boolean validateToken(String token) {
        try {
            Jwts.parser()
                    .verifyWith(getSigningKey())
                    .build()
                    .parseSignedClaims(token);
            return true;
        } catch (Exception e) {
            log.debug("Invalid JWT token: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Get claims from token
     */
    private Claims getClaims(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    /**
     * Get signing key
     */
    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
    }
}
