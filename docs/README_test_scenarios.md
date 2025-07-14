# Test Scenarios Quick Reference

## 📋 **Currently Implemented (17 scenarios)**

### Positive Tests ✅
- ✅ Successful login with valid credentials
- ✅ Social login redirections (Google, Facebook, Apple)

### Negative/Validation Tests ✅  
- ✅ Invalid email + valid password
- ✅ Valid email + invalid password
- ✅ Empty email field validation
- ✅ Empty password field validation  
- ✅ Invalid email format validation (5 formats)

### UI/UX Tests ✅
- ✅ Show/hide password toggle

### Functionality Tests ✅
- ✅ Forgot password link
- ✅ Sign up link

### Session Management ✅
- ✅ Complete login/logout cycle

## 🔄 **Considered but Not Implemented (5 scenarios)**

### UI/UX Tests (Medium Priority)
- 🔄 Login button disabled with empty fields `@skip`
- 🔄 Password field masking validation `@skip`
- 🔄 Mobile responsive design `@skip`

### Security Tests (High Priority)
- 🔄 SQL injection prevention `@skip`
- 🔄 XSS attack prevention `@skip`

## 🏃‍♂️ **Running Tests**

```bash
# Run all implemented tests
behave

# Run only smoke tests
behave --tags=smoke

# Run only positive tests  
behave --tags=positive

# Run only validation tests
behave --tags=validation

# Run quick smoker subset
behave --tags=smoker

# Skip unimplemented scenarios
behave --tags="not skip"
```

## 📊 **Coverage: 77% (17/22 scenarios implemented)**

See [detailed test scenarios documentation](./test_scenarios.md) for complete analysis.
