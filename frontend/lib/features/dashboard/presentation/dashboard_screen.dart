import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Дашборд')),
      body: const Center(
        child: Text('Главный экран приложения'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Navigate to create record screen
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}