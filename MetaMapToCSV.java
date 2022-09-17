import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import gov.nih.nlm.nls.metamap.Ev;
import gov.nih.nlm.nls.metamap.Mapping;
import gov.nih.nlm.nls.metamap.MetaMapApi;
import gov.nih.nlm.nls.metamap.MetaMapApiImpl;
import gov.nih.nlm.nls.metamap.Negation;
import gov.nih.nlm.nls.metamap.PCM;
import gov.nih.nlm.nls.metamap.Result;
import gov.nih.nlm.nls.metamap.Utterance;



/**

/**
 * @author 
 * /opt/public_mm/scripts/metamap_to_csv.jar $input_file $config_file $port_no  > $output_file
 */
public class MetaMapToCSV {

    /**
     * @param args
     */
    public static void main(String[] args)
    {
        String file_name = args[0];
        String config_name = args[1];
        Integer port_out = 8068;

        try {
            String port_in = args[2];
            if (!port_in.contentEquals("")) {
                port_out = Integer.parseInt(port_in);
            }
        } catch (ArrayIndexOutOfBoundsException a) {
            // Do nothing, just use 8066
        }
        catch(Exception e) {
            // If they specified a port and it wasn't correct, then notify.
            e.printStackTrace();
            System.exit(1);
        }

        String mm_args = "";
        try {
            //BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

            // Read in config file
            BufferedReader br = new BufferedReader(new FileReader(config_name));
            String line = "";
            while ((line = br.readLine()) != null){
                mm_args += line;
            }
            //Start the API
            MetaMapApi api = new MetaMapApiImpl();
            api.setPort(port_out);
	    if (mm_args.trim().length() > 2) {
	      api.setOptions(mm_args);
	    }

            // Send in file line by line
            br = new BufferedReader(new FileReader(file_name));
            line = "";
            while ((line = br.readLine()) != null){
                if (line.contentEquals("") || line == null){
                    continue;
                }
                run_metamap(file_name, api, line);
            }
        } catch(IOException io) {
            io.printStackTrace();
        }

        //api.setOptions("-y");
        //api.setOptions("-duy -Q 3");
        //api.setOptions("-duy -Q 3 -J acab,anab,comd,cgab,dsyn,emod,fndg,inpo,mobd,neop,patf,sosy,topp,diap,clna,lbtr,phsu,clnd,antb");
    }
    public static void run_metamap(String file_name, MetaMapApi api, String input)
    {
        try {
            List<Result> resultList = api.processCitationsFromString(input);
            for (Result result: resultList) {
                if (result != null) {
                  List<Negation> negList = result.getNegationList();
                  HashMap<Integer,ArrayList<String>> negMap = new HashMap<Integer, ArrayList<String>>();
                  if (negList.size() > 0) {
                    //System.out.println("Negations:");
                    for (Negation e: negList) {
                        //negMap.put(e.getConceptPositionList().get(0).getX(),
                            //      e.getConceptPairList().get(0).getConceptId());
                        // Trigger
                        ArrayList<String> old_hits = negMap.get(e.getTriggerPositionList().get(0).getX());
                        if (old_hits == null) {
                            old_hits = new ArrayList<String>();
                        }
                        old_hits.add(e.getConceptPairList().get(0).getConceptId());
                        negMap.put(e.getTriggerPositionList().get(0).getX(), old_hits);

                        // Concept
                        old_hits = negMap.get(e.getConceptPositionList().get(0).getX());
                        if (old_hits == null) {
                            old_hits = new ArrayList<String>();
                        }
                        old_hits.add(e.getConceptPairList().get(0).getConceptId());
                        negMap.put(e.getConceptPositionList().get(0).getX(), old_hits);
                    }
                  }
                  for (Utterance utterance: result.getUtteranceList()) {
                    for (PCM pcm: utterance.getPCMList()) {
                        //System.out.println("Mappings:");
                        for (Mapping map: pcm.getMappingList()) {
                          for (Ev mapEv: map.getEvList()) {
                            String negation = "POS";
                            if (!negMap.isEmpty()) {
                                ArrayList<String> CUIs = negMap.get(mapEv.getPositionalInfo().get(0).getX());
                                if ( CUIs != null && CUIs.contains(mapEv.getConceptId()))
                                {
                                    negation = "NEG";
                                }
                            }
                            String cleanPhrase = pcm.getPhrase().getPhraseText().replaceAll("\\|", "");
                            System.out.println(//pcm.getPhrase().getPhraseText() + "|" +
                                                file_name + "|" +
                                                cleanPhrase + "|" +

                                                pcm.getPhrase().getPosition() + "|"
                                                + mapEv.getScore() + "|"
                                                + mapEv.getConceptId() + "|"
                                                + negation + "|"
                                                + mapEv.getConceptName() + "|"
                                                + mapEv.getSemanticTypes() + "|"
                                                + mapEv.getPreferredName() + "|"
                                                + mapEv.getMatchedWords() + "|"
                                                + mapEv.getSources() + "|"
                                                );
                          }
                        }
                      }
                    }
                  } else {
                    System.out.println("NULL result instance! ");
                  }
                }
        } catch (Exception e) {
            System.out.println(e.toString());
        }


    }

}
