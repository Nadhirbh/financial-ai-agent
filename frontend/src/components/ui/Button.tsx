import React from 'react'

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md'
}

const base = 'inline-flex items-center justify-center rounded font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 transition'
const sizes = {
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4 text-sm',
}
const variants = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500 dark:focus-visible:ring-offset-gray-900',
  secondary: 'bg-gray-900 text-white hover:bg-gray-800 focus-visible:ring-gray-500 dark:bg-gray-800 dark:hover:bg-gray-700',
  ghost: 'bg-transparent hover:bg-gray-100 text-gray-900 dark:text-gray-100 dark:hover:bg-gray-800',
}

export default function Button({ variant = 'primary', size = 'md', className = '', ...rest }: Props) {
  return <button className={`${base} ${sizes[size]} ${variants[variant]} ${className}`} {...rest} />
}
