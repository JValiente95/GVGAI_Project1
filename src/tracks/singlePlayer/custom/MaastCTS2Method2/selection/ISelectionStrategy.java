package tracks.singlePlayer.custom.MaastCTS2Method2.selection;

import core.game.StateObservation;
import tools.ElapsedCpuTimer;
import tracks.singlePlayer.custom.MaastCTS2Method2.Server.Server;
import tracks.singlePlayer.custom.MaastCTS2Method2.model.MctNode;
import tracks.singlePlayer.custom.MaastCTS2Method2.test.IPrintableConfig;

public interface ISelectionStrategy extends IPrintableConfig {
	public MctNode select(MctNode rootNode, ElapsedCpuTimer timer, Server server);

	/**
	 * optional method that is called when the agent is initialized.
	 * 
	 * @param so
	 * @param elapsedTimer
	 */
	public void init(StateObservation so, ElapsedCpuTimer elapsedTimer);
	
	/**
	 * Should be implemented to return the maximum desired size of n-grams of actions
	 * to collect statistics for.
	 * 
	 * <p> If a value < 1 is returned, will not collect statistics for any n-grams
	 * 
	 * @return
	 */
	public int getDesiredActionNGramSize();
	
	/**
	 * Should be implemented to return true iff the selection strategy requires
	 * action statistics to be backpropagated (for example, Progressive History)
	 * 
	 * @return
	 */
	public boolean wantsActionStatistics();
}
