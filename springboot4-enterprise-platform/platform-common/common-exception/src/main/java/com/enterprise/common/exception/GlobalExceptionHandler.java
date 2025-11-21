package com.enterprise.common.exception;

import com.enterprise.common.core.result.Result;
import com.enterprise.common.core.result.ResultCode;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.resource.NoResourceFoundException;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import java.util.stream.Collectors;

/**
 * Global Exception Handler
 * Handles all exceptions and returns unified response
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handle BaseException
     */
    @ExceptionHandler(BaseException.class)
    @ResponseStatus(HttpStatus.OK)
    public Result<?> handleBaseException(BaseException e, HttpServletRequest request) {
        log.error("BaseException occurred: {} - {}", e.getCode(), e.getMessage(), e);
        return Result.failure(e.getCode(), e.getMessage())
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle BusinessException
     */
    @ExceptionHandler(BusinessException.class)
    @ResponseStatus(HttpStatus.OK)
    public Result<?> handleBusinessException(BusinessException e, HttpServletRequest request) {
        log.warn("BusinessException occurred: {}", e.getMessage());
        return Result.failure(e.getCode(), e.getMessage())
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle validation errors (MethodArgumentNotValidException)
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result<?> handleValidationException(MethodArgumentNotValidException e, HttpServletRequest request) {
        String errorMessage = e.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining("; "));
        log.warn("Validation error: {}", errorMessage);
        return Result.failure(ResultCode.VALIDATION_ERROR, errorMessage)
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle BindException
     */
    @ExceptionHandler(BindException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result<?> handleBindException(BindException e, HttpServletRequest request) {
        String errorMessage = e.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining("; "));
        log.warn("Bind error: {}", errorMessage);
        return Result.failure(ResultCode.VALIDATION_ERROR, errorMessage)
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle ConstraintViolationException
     */
    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result<?> handleConstraintViolationException(ConstraintViolationException e, HttpServletRequest request) {
        String errorMessage = e.getConstraintViolations().stream()
                .map(ConstraintViolation::getMessage)
                .collect(Collectors.joining("; "));
        log.warn("Constraint violation: {}", errorMessage);
        return Result.failure(ResultCode.VALIDATION_ERROR, errorMessage)
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle MethodArgumentTypeMismatchException
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result<?> handleMethodArgumentTypeMismatchException(MethodArgumentTypeMismatchException e, HttpServletRequest request) {
        String errorMessage = String.format("Parameter '%s' should be of type %s",
                e.getName(),
                e.getRequiredType() != null ? e.getRequiredType().getSimpleName() : "unknown");
        log.warn("Method argument type mismatch: {}", errorMessage);
        return Result.failure(ResultCode.BAD_REQUEST, errorMessage)
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle NoResourceFoundException (404)
     */
    @ExceptionHandler(NoResourceFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public Result<?> handleNoResourceFoundException(NoResourceFoundException e, HttpServletRequest request) {
        log.warn("Resource not found: {}", e.getMessage());
        return Result.failure(ResultCode.NOT_FOUND)
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle IllegalArgumentException
     */
    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result<?> handleIllegalArgumentException(IllegalArgumentException e, HttpServletRequest request) {
        log.warn("Illegal argument: {}", e.getMessage());
        return Result.failure(ResultCode.BAD_REQUEST, e.getMessage())
                .withTraceId(getTraceId(request));
    }

    /**
     * Handle all other exceptions
     */
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public Result<?> handleException(Exception e, HttpServletRequest request) {
        log.error("Unexpected error occurred", e);
        return Result.failure(ResultCode.INTERNAL_SERVER_ERROR, "An unexpected error occurred")
                .withTraceId(getTraceId(request));
    }

    /**
     * Get trace ID from request
     */
    private String getTraceId(HttpServletRequest request) {
        String traceId = request.getHeader("X-Trace-Id");
        if (traceId == null || traceId.isBlank()) {
            traceId = request.getHeader("X-Request-Id");
        }
        return traceId;
    }
}
