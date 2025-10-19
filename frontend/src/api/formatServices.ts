/**
 * Форматирует строку с датой в русский формат (ДД.ММ.ГГГГ).
 * Корректно обрабатывает разные входящие форматы (YYYY-MM-DD, MM/DD/YYYY и др.),
 * которые может распознать конструктор Date.
 *
 * @param dateString - Строка с датой, null или undefined.
 * @returns - Дата в формате "ДД.ММ.ГГГГ" или пустая строка, если дата невалидна.
 */
export function formatDateToRu(dateString: string | null | undefined): string {
  if (!dateString) {
    return ''
  }
  const date = new Date(dateString)

  if (isNaN(date.getTime())) {
    return ''
  }

  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date)
}
