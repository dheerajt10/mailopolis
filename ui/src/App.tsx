import { BaseLayout } from './layout/BaseLayout';
import { GameProvider } from './contexts/GameContext';

function App() {
  return (
    <GameProvider>
      <BaseLayout />
    </GameProvider>
  );
}

export default App;
