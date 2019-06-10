/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.gephi.toolkit.demos;

import java.awt.Color;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URISyntaxException;
import org.gephi.appearance.api.AppearanceController;
import org.gephi.appearance.api.AppearanceModel;
import org.gephi.appearance.api.Function;
import org.gephi.appearance.api.Partition;
import org.gephi.appearance.api.PartitionFunction;
import org.gephi.appearance.plugin.PartitionElementColorTransformer;
import org.gephi.appearance.plugin.palette.Palette;
import org.gephi.appearance.plugin.palette.PaletteManager;
import org.gephi.filters.api.FilterController;
import org.gephi.filters.api.Query;
import org.gephi.filters.plugin.graph.DegreeRangeBuilder;
import org.gephi.filters.plugin.partition.PartitionBuilder;
import org.gephi.graph.api.Column;
import org.gephi.graph.api.DirectedGraph;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.GraphView;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.spi.GraphExporter;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.EdgeDirectionDefault;
import org.gephi.io.importer.api.EdgeMergeStrategy;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.AppendProcessor;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.preview.api.PreviewProperty;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.statistics.plugin.Modularity;
import org.openide.util.Lookup;

/**
 *
 * @author tanmay
 */
public class trial {
    
    public void multipleCalls(){
        String authorName = "andrewlewis@google.com";
        script("01", authorName);
        script("02", authorName);
        script("03", authorName);
        script("04", authorName);
        script("05", authorName);
        script("06", authorName);
        script("07", authorName);
        script("08", authorName);
        script("09", authorName);
        script("10", authorName);
        script("11", authorName);
        script("12", authorName);
    }
    
    public void script(String parameter, String authorname){
        
        //Init a project - and therefore a workspace
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();

        //Get models and controllers for this new workspace - will be useful later
        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        GraphModel graphModel = Lookup.getDefault().lookup(GraphController.class).getGraphModel();
        AppearanceController appearanceController = Lookup.getDefault().lookup(AppearanceController.class);
        AppearanceModel appearanceModel = appearanceController.getModel();
        FilterController filterController = Lookup.getDefault().lookup(FilterController.class);
        DegreeRangeBuilder.DegreeRangeFilter degreeFilter = new DegreeRangeBuilder.DegreeRangeFilter();
         PreviewModel previewModel = Lookup.getDefault().lookup(PreviewController.class).getModel();
       previewModel.getProperties().putValue(PreviewProperty.SHOW_NODE_LABELS, Boolean.TRUE);
       previewModel.getProperties().putValue(PreviewProperty.VISIBILITY_RATIO, 0.1);
        previewModel.getProperties().putValue(PreviewProperty.DIRECTED, Boolean.TRUE);
        previewModel.getProperties().putValue(PreviewProperty.NODE_LABEL_PROPORTIONAL_SIZE, Boolean.FALSE);
        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
        
        Layout l = new Layout();

    //Import file
    Container container,container2;
    try {
        System.out.println("/org/gephi/toolkit/demos/exoplayer/"+ authorname + "/" + parameter + "-2016nodes.csv");
        File file_node =  new File(getClass().getResource("/org/gephi/toolkit/demos/exoplayer/"+ authorname + "/" + parameter + "-2016nodes.csv").toURI());
        container = importController.importFile(file_node);
        container.getLoader().setEdgeDefault(EdgeDirectionDefault.DIRECTED);   //Force DIRECTED
        //container.getLoader().setAllowAutoNode(true);  //create missing nodes
        container.getLoader().setEdgesMergeStrategy(EdgeMergeStrategy.SUM);
        container.getLoader().setAutoScale(true);

        File file_edge =  new File(getClass().getResource("/org/gephi/toolkit/demos/exoplayer/"+ authorname + "/" + parameter + "-2016edges.csv").toURI());
        container2 = importController.importFile(file_edge);
        container2.getLoader().setEdgeDefault(EdgeDirectionDefault.DIRECTED);   //Force DIRECTED
        //container2.getLoader().setAllowAutoNode(true);  //create missing nodes
       container2.getLoader().setEdgesMergeStrategy(EdgeMergeStrategy.SUM);
       container2.getLoader().setAutoScale(true);

    } catch (FileNotFoundException ex) {
        return;
    }   catch (URISyntaxException ex) {
        return;
        }
    
     //Append imported data to GraphAPI
    importController.process(container, new DefaultProcessor(), workspace);
    importController.process(container2, new AppendProcessor(), workspace); //Use AppendProcessor to append to current workspace
    
    DirectedGraph graph = graphModel.getDirectedGraph();
    System.out.println("Nodes: " + graph.getNodeCount());
    System.out.println("Edges: " + graph.getEdgeCount());  
    
    //Partition with 'source' column, which is in the data
        Column column = graphModel.getNodeTable().getColumn("dev");
        Function func = appearanceModel.getNodeFunction(graph, column, PartitionElementColorTransformer.class);
        Partition partition = ((PartitionFunction) func).getPartition();
        System.out.println(partition.size() + " partitions found");
        Palette palette = PaletteManager.getInstance().generatePalette(partition.size());
        Color[] colors2 = new Color[2];
         colors2[0] = Color.LIGHT_GRAY;
         colors2[1] = Color.MAGENTA; 
        
        Color[] colors3 = new Color[3];
        colors3[0] = Color.LIGHT_GRAY;
         colors3[1] = Color.PINK; 
         colors3[2] = Color.MAGENTA;
         if(partition.size() == 2 )
             partition.setColors(colors2);
         else
            partition.setColors(colors3);
        appearanceController.transform(func);

        //Export
        try {
            ec.exportFile(new File(authorname + parameter + "-2016withlabels.pdf"));
        } catch (IOException ex) {
        }
        
         //Export only visible graph
        GraphExporter exporter = (GraphExporter) ec.getExporter("gexf");     //Get GEXF exporter
        exporter.setExportVisible(true);  //Only exports the visible (filtered) graph
        exporter.setWorkspace(workspace);
        try {
            ec.exportFile(new File(authorname + parameter + "-2016withlabels.gexf"), exporter);
        } catch (IOException ex) {
            return;
        }
        
        previewModel.getProperties().putValue(PreviewProperty.SHOW_NODE_LABELS, Boolean.FALSE);
        
        try {
            ec.exportFile(new File(authorname + parameter + "-2016withoutlabels.pdf"));
        } catch (IOException ex) {
        }
        
         //Export only visible graph
        exporter = (GraphExporter) ec.getExporter("gexf");     //Get GEXF exporter
        exporter.setExportVisible(true);  //Only exports the visible (filtered) graph
        exporter.setWorkspace(workspace);
        try {
            ec.exportFile(new File(authorname + parameter + "-2016withoutlabels.gexf"), exporter);
        } catch (IOException ex) {
            return;
        }
    }
}