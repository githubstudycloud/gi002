package service

import (
	"context"
	"fmt"

	"github.com/yourname/go-enterprise-platform/internal/user/model"
	"github.com/yourname/go-enterprise-platform/internal/user/repository"
	"github.com/yourname/go-enterprise-platform/pkg/errors"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

// UserService 用户服务接口
type UserService interface {
	Register(ctx context.Context, req *model.CreateUserRequest) (*model.User, error)
	Login(ctx context.Context, req *model.LoginRequest) (*model.LoginResponse, error)
	GetUser(ctx context.Context, id uint) (*model.User, error)
	UpdateUser(ctx context.Context, id uint, req *model.UpdateUserRequest) (*model.User, error)
	DeleteUser(ctx context.Context, id uint) error
	ListUsers(ctx context.Context, page, pageSize int) ([]*model.User, int64, error)
}

type userService struct {
	repo repository.UserRepository
}

// NewUserService 创建用户服务
func NewUserService(repo repository.UserRepository) UserService {
	return &userService{repo: repo}
}

func (s *userService) Register(ctx context.Context, req *model.CreateUserRequest) (*model.User, error) {
	// 检查用户名是否已存在
	if _, err := s.repo.GetByUsername(ctx, req.Username); err == nil {
		return nil, errors.New(errors.ErrUserAlreadyExists, "username already exists")
	} else if err != gorm.ErrRecordNotFound {
		return nil, errors.Wrap(errors.ErrDatabase, "failed to check username", err)
	}

	// 检查邮箱是否已存在
	if _, err := s.repo.GetByEmail(ctx, req.Email); err == nil {
		return nil, errors.New(errors.ErrUserAlreadyExists, "email already exists")
	} else if err != gorm.ErrRecordNotFound {
		return nil, errors.Wrap(errors.ErrDatabase, "failed to check email", err)
	}

	// 密码加密
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, errors.Wrap(errors.ErrInternalServer, "failed to hash password", err)
	}

	// 创建用户
	user := &model.User{
		Username: req.Username,
		Email:    req.Email,
		Password: string(hashedPassword),
		Nickname: req.Nickname,
		Status:   1,
	}

	if err := s.repo.Create(ctx, user); err != nil {
		return nil, errors.Wrap(errors.ErrDatabase, "failed to create user", err)
	}

	return user, nil
}

func (s *userService) Login(ctx context.Context, req *model.LoginRequest) (*model.LoginResponse, error) {
	// 获取用户
	user, err := s.repo.GetByUsername(ctx, req.Username)
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, errors.New(errors.ErrUserNotFound, "user not found")
		}
		return nil, errors.Wrap(errors.ErrDatabase, "failed to get user", err)
	}

	// 验证密码
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(req.Password)); err != nil {
		return nil, errors.New(errors.ErrInvalidPassword, "invalid password")
	}

	// 检查用户状态
	if user.Status != 1 {
		return nil, errors.New(errors.ErrUserDisabled, "user is disabled")
	}

	// TODO: 生成 JWT Token
	token := fmt.Sprintf("mock-token-%d", user.ID)

	return &model.LoginResponse{
		Token: token,
		User:  user,
	}, nil
}

func (s *userService) GetUser(ctx context.Context, id uint) (*model.User, error) {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, errors.New(errors.ErrUserNotFound, "user not found")
		}
		return nil, errors.Wrap(errors.ErrDatabase, "failed to get user", err)
	}
	return user, nil
}

func (s *userService) UpdateUser(ctx context.Context, id uint, req *model.UpdateUserRequest) (*model.User, error) {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, errors.New(errors.ErrUserNotFound, "user not found")
		}
		return nil, errors.Wrap(errors.ErrDatabase, "failed to get user", err)
	}

	// 更新字段
	if req.Nickname != "" {
		user.Nickname = req.Nickname
	}
	if req.Avatar != "" {
		user.Avatar = req.Avatar
	}

	if err := s.repo.Update(ctx, user); err != nil {
		return nil, errors.Wrap(errors.ErrDatabase, "failed to update user", err)
	}

	return user, nil
}

func (s *userService) DeleteUser(ctx context.Context, id uint) error {
	if err := s.repo.Delete(ctx, id); err != nil {
		return errors.Wrap(errors.ErrDatabase, "failed to delete user", err)
	}
	return nil
}

func (s *userService) ListUsers(ctx context.Context, page, pageSize int) ([]*model.User, int64, error) {
	offset := (page - 1) * pageSize
	users, total, err := s.repo.List(ctx, offset, pageSize)
	if err != nil {
		return nil, 0, errors.Wrap(errors.ErrDatabase, "failed to list users", err)
	}
	return users, total, nil
}
