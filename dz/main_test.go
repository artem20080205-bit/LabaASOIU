package main

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// Проверяем полный цикл между отдельными вызовами команд.
func TestPersistence(t *testing.T) {
	path := filepath.Join(t.TempDir(), "tasks.json")
	var out bytes.Buffer
	commands := [][]string{
		{"add", "Изучить Go"}, {"add", "Сдать ДЗ"}, {"done", "1"},
	}
	for _, args := range commands {
		if err := run(path, args, &out); err != nil {
			t.Fatal(err)
		}
	}
	tasks, err := loadTasks(path)
	if err != nil || len(tasks) != 2 {
		t.Fatalf("не удалось восстановить задачи: %v, %v", tasks, err)
	}
	if !tasks[0].Done || tasks[1].Done || tasks[1].ID != 2 {
		t.Fatalf("неверные данные: %+v", tasks)
	}
	out.Reset()
	if err := run(path, []string{"stats"}, &out); err != nil {
		t.Fatal(err)
	}
	if out.String() != "Всего: 2; выполнено: 1; осталось: 1\n" {
		t.Fatal(out.String())
	}
}

// Ошибочная команда не должна менять сохраненные данные.
func TestInvalidCommandDoesNotChangeFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "tasks.json")
	var out bytes.Buffer
	if err := run(path, []string{"add", "Задача"}, &out); err != nil {
		t.Fatal(err)
	}
	before, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	for _, args := range [][]string{
		{"add", " "}, {"done", "abc"}, {"done", "99"},
		{"done"}, {"list", "extra"}, {"unknown"},
	} {
		if err := run(path, args, &out); err == nil {
			t.Fatalf("ожидалась ошибка: %v", args)
		}
	}
	after, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(before, after) {
		t.Fatal("файл изменился")
	}
}

func TestCorruptFileIsPreserved(t *testing.T) {
	path := filepath.Join(t.TempDir(), "tasks.json")
	before := []byte("broken json")
	if err := os.WriteFile(path, before, 0644); err != nil {
		t.Fatal(err)
	}
	var out bytes.Buffer
	if err := run(path, []string{"add", "Задача"}, &out); err == nil {
		t.Fatal("ожидалась ошибка чтения")
	}
	after, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(before, after) {
		t.Fatal("поврежденный файл перезаписан")
	}
}

func TestEmptyList(t *testing.T) {
	path := filepath.Join(t.TempDir(), "tasks.json")
	var out bytes.Buffer
	if err := run(path, []string{"list"}, &out); err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(out.String(), "Список задач пуст.") {
		t.Fatal(out.String())
	}
	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Fatal("чтение пустого списка создало файл")
	}
}
