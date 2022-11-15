import React from 'react'

export const Error = ({
  message
}) => {
  return (
    <div>
      <h1>Ошибка {message?.response?.status}</h1>

      <div>{message?.message}</div>
      <div>{message?.response?.data?.detail}</div>
    </div>
  )
}
