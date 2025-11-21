package handler

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/yourname/go-enterprise-platform/internal/user/model"
	"github.com/yourname/go-enterprise-platform/internal/user/service"
	"github.com/yourname/go-enterprise-platform/pkg/errors"
)

// UserHandler 用户处理器
type UserHandler struct {
	service service.UserService
}

// NewUserHandler 创建用户处理器
func NewUserHandler(service service.UserService) *UserHandler {
	return &UserHandler{service: service}
}

// RegisterRoutes 注册路由
func (h *UserHandler) RegisterRoutes(r *gin.RouterGroup) {
	users := r.Group("/users")
	{
		users.POST("/register", h.Register)
		users.POST("/login", h.Login)
		users.GET("/:id", h.GetUser)
		users.PUT("/:id", h.UpdateUser)
		users.DELETE("/:id", h.DeleteUser)
		users.GET("", h.ListUsers)
	}
}

// Register 用户注册
func (h *UserHandler) Register(c *gin.Context) {
	var req model.CreateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, errors.Fail(errors.ErrInvalidParams, err.Error()))
		return
	}

	user, err := h.service.Register(c.Request.Context(), &req)
	if err != nil {
		if appErr, ok := err.(*errors.AppError); ok {
			c.JSON(appErr.HTTPStatus(), errors.Fail(appErr.Code, appErr.Message))
			return
		}
		c.JSON(http.StatusInternalServerError, errors.Fail(errors.ErrInternalServer, err.Error()))
		return
	}

	c.JSON(http.StatusOK, errors.Success(user))
}

// Login 用户登录
func (h *UserHandler) Login(c *gin.Context) {
	var req model.LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, errors.Fail(errors.ErrInvalidParams, err.Error()))
		return
	}

	resp, err := h.service.Login(c.Request.Context(), &req)
	if err != nil {
		if appErr, ok := err.(*errors.AppError); ok {
			c.JSON(appErr.HTTPStatus(), errors.Fail(appErr.Code, appErr.Message))
			return
		}
		c.JSON(http.StatusInternalServerError, errors.Fail(errors.ErrInternalServer, err.Error()))
		return
	}

	c.JSON(http.StatusOK, errors.Success(resp))
}

// GetUser 获取用户
func (h *UserHandler) GetUser(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, errors.Fail(errors.ErrInvalidParams, "invalid user id"))
		return
	}

	user, err := h.service.GetUser(c.Request.Context(), uint(id))
	if err != nil {
		if appErr, ok := err.(*errors.AppError); ok {
			c.JSON(appErr.HTTPStatus(), errors.Fail(appErr.Code, appErr.Message))
			return
		}
		c.JSON(http.StatusInternalServerError, errors.Fail(errors.ErrInternalServer, err.Error()))
		return
	}

	c.JSON(http.StatusOK, errors.Success(user))
}

// UpdateUser 更新用户
func (h *UserHandler) UpdateUser(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, errors.Fail(errors.ErrInvalidParams, "invalid user id"))
		return
	}

	var req model.UpdateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, errors.Fail(errors.ErrInvalidParams, err.Error()))
		return
	}

	user, err := h.service.UpdateUser(c.Request.Context(), uint(id), &req)
	if err != nil {
		if appErr, ok := err.(*errors.AppError); ok {
			c.JSON(appErr.HTTPStatus(), errors.Fail(appErr.Code, appErr.Message))
			return
		}
		c.JSON(http.StatusInternalServerError, errors.Fail(errors.ErrInternalServer, err.Error()))
		return
	}

	c.JSON(http.StatusOK, errors.Success(user))
}

// DeleteUser 删除用户
func (h *UserHandler) DeleteUser(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, errors.Fail(errors.ErrInvalidParams, "invalid user id"))
		return
	}

	if err := h.service.DeleteUser(c.Request.Context(), uint(id)); err != nil {
		if appErr, ok := err.(*errors.AppError); ok {
			c.JSON(appErr.HTTPStatus(), errors.Fail(appErr.Code, appErr.Message))
			return
		}
		c.JSON(http.StatusInternalServerError, errors.Fail(errors.ErrInternalServer, err.Error()))
		return
	}

	c.JSON(http.StatusOK, errors.Success(nil))
}

// ListUsers 用户列表
func (h *UserHandler) ListUsers(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	pageSize, _ := strconv.Atoi(c.DefaultQuery("page_size", "10"))

	if page < 1 {
		page = 1
	}
	if pageSize < 1 || pageSize > 100 {
		pageSize = 10
	}

	users, total, err := h.service.ListUsers(c.Request.Context(), page, pageSize)
	if err != nil {
		if appErr, ok := err.(*errors.AppError); ok {
			c.JSON(appErr.HTTPStatus(), errors.Fail(appErr.Code, appErr.Message))
			return
		}
		c.JSON(http.StatusInternalServerError, errors.Fail(errors.ErrInternalServer, err.Error()))
		return
	}

	c.JSON(http.StatusOK, errors.Success(gin.H{
		"list":  users,
		"total": total,
		"page":  page,
		"page_size": pageSize,
	}))
}
