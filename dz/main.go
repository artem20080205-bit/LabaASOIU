// Консольный список задач с сохранением в JSON.
package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

// Task объединяет данные одной задачи. Теги задают имена полей JSON.
type Task struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
	Done  bool   `json:"done"`
}

// Отсутствие файла при первом запуске означает пустой список.
func loadTasks(path string) ([]Task, error) {
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return []Task{}, nil
	}
	if err != nil {
		return nil, err
	}
	var tasks []Task
	if err := json.Unmarshal(data, &tasks); err != nil {
		return nil, fmt.Errorf("не удалось прочитать JSON: %w", err)
	}
	return tasks, nil
}

// Кодирование выполняется до записи, чтобы проверить данные заранее.
func saveTasks(path string, tasks []Task) error {
	data, err := json.MarshalIndent(tasks, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, append(data, '\n'), 0644)
}

// Новый идентификатор больше всех уже сохраненных идентификаторов.
func nextID(tasks []Task) int {
	id := 1
	for _, task := range tasks {
		if task.ID >= id {
			id = task.ID + 1
		}
	}
	return id
}

// run отделяет обработку команд от завершения процесса в main.
// io.Writer позволяет использовать ту же функцию в автоматических тестах.
func run(path string, args []string, out io.Writer) error {
	if len(args) == 0 {
		fmt.Fprintln(out, "Команды: add <текст> | list | done <id> | stats")
		return nil
	}
	tasks, err := loadTasks(path)
	if err != nil {
		return err
	}
	switch args[0] {
	case "add":
		// Слова команды объединяются в название; пробельный текст запрещен.
		title := strings.TrimSpace(strings.Join(args[1:], " "))
		if title == "" {
			return fmt.Errorf("укажите непустой текст задачи")
		}
		task := Task{ID: nextID(tasks), Title: title}
		if err := saveTasks(path, append(tasks, task)); err != nil {
			return err
		}
		fmt.Fprintf(out, "Добавлена задача %d: %s\n", task.ID, task.Title)
	case "list":
		// Чтение списка не создает и не изменяет файл.
		if len(args) != 1 {
			return fmt.Errorf("команда list не принимает аргументы")
		}
		if len(tasks) == 0 {
			fmt.Fprintln(out, "Список задач пуст.")
		}
		for _, task := range tasks {
			mark := " "
			if task.Done {
				mark = "x"
			}
			fmt.Fprintf(out, "%d. [%s] %s\n", task.ID, mark, task.Title)
		}
	case "done":
		// Поиск идет по ID, а не по позиции задачи в срезе.
		if len(args) != 2 {
			return fmt.Errorf("использование: done <id>")
		}
		id, err := strconv.Atoi(args[1])
		if err != nil || id <= 0 {
			return fmt.Errorf("id должен быть положительным целым числом")
		}
		for i := range tasks {
			if tasks[i].ID == id {
				tasks[i].Done = true
				if err := saveTasks(path, tasks); err != nil {
					return err
				}
				fmt.Fprintf(out, "Задача %d выполнена.\n", id)
				return nil
			}
		}
		return fmt.Errorf("задача %d не найдена", id)
	case "stats":
		// Подсчитываем выполненные задачи обычным циклом range.
		if len(args) != 1 {
			return fmt.Errorf("команда stats не принимает аргументы")
		}
		done := 0
		for _, task := range tasks {
			if task.Done {
				done++
			}
		}
		fmt.Fprintf(out, "Всего: %d; выполнено: %d; осталось: %d\n",
			len(tasks), done, len(tasks)-done)
	default:
		return fmt.Errorf("неизвестная команда: %s", args[0])
	}
	return nil
}

// Флаги задаются перед командой: tasker -file tasks.json list.
func main() {
	path := flag.String("file", "tasks.json", "путь к файлу задач")
	flag.Parse()
	if err := run(*path, flag.Args(), os.Stdout); err != nil {
		fmt.Fprintln(os.Stderr, "Ошибка:", err)
		os.Exit(1)
	}
}
