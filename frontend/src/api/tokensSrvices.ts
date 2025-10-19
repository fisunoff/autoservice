function safelyParseJSON(jsonString: string | null) {
  if (!jsonString) {
    return null
  }
  try {
    return JSON.parse(jsonString)
  } catch (e) {
    console.error('Failed to parse user from localStorage', e)
    return null
  }
}

export function getLocalRefreshToken() {
  const user = safelyParseJSON(localStorage.getItem('user'))
  return user?.refreshToken
}

export function getLocalAccessToken() {
  const user = safelyParseJSON(localStorage.getItem('user'))
  return user?.accessToken
}

export function getUser() {
  return safelyParseJSON(localStorage.getItem('user'))
}

export function setUser(accessToken: string, refreshToken: string) {
  const user = { accessToken, refreshToken }
  localStorage.setItem('user', JSON.stringify(user))
}

export function removeUser() {
  localStorage.removeItem('user')
}
