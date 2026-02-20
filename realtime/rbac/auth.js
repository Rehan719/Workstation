// Role-Based Access Control logic for Jules AI
const permissions = require('./permissions.json');

function checkPermission(role, action) {
  const rolePermissions = permissions[role];
  if (!rolePermissions) return false;
  return rolePermissions.includes(action) || rolePermissions.includes('*');
}

module.exports = {
  checkPermission,
  roles: Object.keys(permissions)
};
